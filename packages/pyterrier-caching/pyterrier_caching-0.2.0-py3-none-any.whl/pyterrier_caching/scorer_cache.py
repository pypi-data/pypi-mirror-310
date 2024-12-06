from typing import Optional
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
import pyterrier as pt
import shutil
import json
import sqlite3
from collections import defaultdict
from contextlib import closing, contextmanager
from npids import Lookup
from deprecated import deprecated
from pyterrier_caching import BuilderMode, artifact_builder, meta_file_compat
import pyterrier_alpha as pta


class Hdf5ScorerCache(pta.Artifact, pt.Transformer):
    artifact_type = 'scorer_cache'
    artifact_format = 'hdf5'

    def __init__(self, path, scorer=None, verbose=False):
        super().__init__(path)
        meta_file_compat(path)
        self.mode = 'r'
        self.scorer = scorer
        self.verbose = verbose
        self.meta = None
        self.file = None
        self.docnos = None
        self.dataset_cache = {}

    def transform(self, inp):
        return self.cached_scorer()(inp)

    def built(self) -> bool:
        return (Path(self.path)/'pt_meta.json').exists()

    def build(self, corpus_iter=None, docnos_file=None):
        assert not self.built(), "this cache is alrady built"
        assert corpus_iter is not None or docnos_file is not None
        import h5py
        with artifact_builder(self.path, BuilderMode.create, self.artifact_type, self.artifact_format) as builder:
            with h5py.File(str(builder.path/'data.h5'), 'a'):
                pass # just create the data file
            if docnos_file:
                shutil.copy(docnos_file, builder.path/'docnos.npids')
                builder.metadata['doc_count'] = len(Lookup(builder.path/'docnos.npids'))
            else:
                builder.metadata['doc_count'] = 0
                with Lookup.builder(builder.path/'docnos.npids') as docno_lookup:
                    for record in corpus_iter:
                        docno_lookup.add(record['docno'])
                        builder.metadata['doc_count'] += 1

    def _ensure_built(self):
        import h5py
        assert self.built(), "you must .build(...) this cache before it can be used"
        if self.file is None:
            self.file = h5py.File(self.path/'data.h5', self.mode)
        if self.meta is None:
            with (self.path/'pt_meta.json').open('rt') as fin:
                self.meta = json.load(fin)
        if self.docnos is None:
            self.docnos = Lookup(self.path/'docnos.npids')

    def _ensure_write_mode(self):
        if self.mode == 'r':
            if self.scorer is None:
                raise LookupError('values missing from cache, but no scorer provided')
            import h5py
            self.mode = 'a'
            self.file.close()
            self.file = h5py.File(self.path/'data.h5', self.mode)
            self.dataset_cache = {} # file changed, need to reset the cache

    def _get_dataset(self, qid):
        if qid not in self.dataset_cache:
            if qid not in self.file:
                self._ensure_write_mode()
                # TODO: setting chunks=(4096,) --- or some other value? --- might help
                # reduce the file size and/or speed up writes? Investigate more...
                self.file.create_dataset(qid, shape=(self.corpus_count(),), dtype=np.float32, fillvalue=float('nan'))
            self.dataset_cache[qid] = self.file[qid]
        return self.dataset_cache[qid]

    def corpus_count(self):
        self._ensure_built()
        return self.meta['doc_count']

    def __repr__(self):
        return f'Hdf5ScorerCache({repr(str(self.path))}, {self.scorer})'

    def cached_scorer(self) -> pt.Transformer:
        return Hdf5ScorerCacheScorer(self)

    def cached_retriever(self, num_results: int = 1000) -> pt.Transformer:
        return Hdf5ScorerCacheRetriever(self, num_results)


class Hdf5ScorerCacheScorer(pt.Transformer):
    def __init__(self, cache: Hdf5ScorerCache):
        self.cache = cache

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        self.cache._ensure_built()
        results = []
        misses = 0
        for query, group in inp.groupby('query'):
            query_hash = hashlib.sha256(query.encode()).hexdigest()
            ds = self.cache._get_dataset(query_hash)
            dids = self.cache.docnos.inv[np.array(group.docno)]
            dids_sorted, undo_did_sort = np.unique(dids, return_inverse=True)
            scores = ds[dids_sorted][undo_did_sort]
            to_score = group.loc[group.docno[np.isnan(scores)].index]
            misses += len(to_score)
            if len(to_score) > 0:
                self.cache._ensure_write_mode()
                ds = self.cache._get_dataset(query_hash)
                new_scores = self.cache.scorer(to_score)
                dids = self.cache.docnos.inv[np.array(new_scores.docno)]
                dids_sorted, dids_sorted_idx = np.unique(dids, return_index=True)
                ds[dids_sorted] = new_scores.score.iloc[dids_sorted_idx]
                dids = self.cache.docnos.inv[np.array(group.docno)]
                dids_sorted, undo_did_sort = np.unique(dids, return_inverse=True)
                scores = ds[dids_sorted][undo_did_sort]
            results.append(group.assign(score=scores))
        results = pd.concat(results, ignore_index=True)
        pt.model.add_ranks(results)
        if self.cache.verbose:
            print(f"{self}: {len(inp)-misses} hit(s), {misses} miss(es)")
        return results


class Hdf5ScorerCacheRetriever(pt.Transformer):
    def __init__(self, cache: Hdf5ScorerCache, num_results: int = 1000):
        self.cache = cache
        self.num_results = num_results

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        self.cache._ensure_built()
        pta.validate.query_frame(inp, extra_columns=['query'])
        inp = inp.reset_index(drop=True)
        builder = pta.DataFrameBuilder(['_index', 'docno', 'score', 'rank'])
        for i, query in enumerate(inp['query']):
            query_hash = hashlib.sha256(query.encode()).hexdigest()
            ds = self.cache._get_dataset(query_hash)[:]
            nans = np.isnan(ds)
            if nans.any():
                raise RuntimeError(f'retriever only works if corpus is scored completely; '
                                   f'{nans.sum()} uncached documents found for query {query!r}.')
            k = min(len(ds), self.num_results)
            docids = ds.argpartition(-k)[-k:]
            scores = ds[docids]
            idxs = scores.argsort()[::-1]
            builder.extend({
                '_index': i,
                'docno': self.cache.docnos.fwd[docids[idxs]],
                'score': scores[idxs],
                'rank': np.arange(scores.shape[0]),
            })
        return builder.to_df(merge_on_index=inp)


class Sqlite3ScorerCache(pta.Artifact, pt.Transformer):
    """ A cache for storing and retrieving scores for documents, backed by a SQLite3 database. """

    artifact_type = 'scorer_cache'
    artifact_format = 'sqlite3'

    def __init__(
        self,
        path: str,
        scorer: pt.Transformer = None,
        *,
        group: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        verbose: bool = False
    ):
        """ Creates a new Sqlite3ScorerCache instance.

        If a cache does not yet exist at the provided ``path``, a new one is created.

        Args:
            path: The path to the directory where the cache should be stored.
            scorer: The scorer to use to score documents that are missing from the cache.
            group: The name of the column in the input DataFrame that contains the group identifier (default: ``query``)
            key: The name of the column in the input DataFrame that contains the document identifier (default: ``docno``)
            value: The name of the column in the input DataFrame that contains the value to cache (default: ``score``)
        """
        super().__init__(path)
        meta_file_compat(path)
        self.scorer = scorer
        self.verbose = verbose
        self.meta = None
        if not (Path(self.path)/'pt_meta.json').exists():
            if group is None:
                group = 'query'
            if key is None:
                key = 'docno'
            if value is None:
                value = 'score'
            with artifact_builder(self.path, BuilderMode.create, self.artifact_type, self.artifact_format) as builder:
                builder.metadata['group'] = group
                builder.metadata['key'] = key
                builder.metadata['value'] = value
                self.db = sqlite3.connect(builder.path/'db.sqlite3')
                with closing(self.db.cursor()) as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS cache (
                          [group] TEXT NOT NULL,
                          key TEXT NOT NULL,
                          value NUMERIC NOT NULL,
                          PRIMARY KEY ([group], key)
                        )
                    """)
        else:
            self.db = sqlite3.connect(self.path/'db.sqlite3')
        with (Path(self.path)/'pt_meta.json').open('rt') as fin:
            self.meta = json.load(fin)
        if group is not None:
            assert group == self.meta['group'], f'group={group!r} provided, but index created with group={self.meta["group"]!r}'
        self.group = self.meta['group']
        if key is not None:
            assert key == self.meta['key'], f'key={key!r} provided, but index created with key={self.meta["key"]!r}'
        self.key = self.meta['key']
        if value is not None:
            assert value == self.meta['value'], f'value={value!r} provided, but index created with value={self.meta["value"]!r}'
        self.value = self.meta['value']

    def close(self):
        """ Closes this cache, releasing the sqlite connection that it holds. """
        if self.db is not None:
            self.db.close()
            self.db = None

    @contextmanager
    def _cursor(self):
        assert self.db is not None, "cache is closed"
        with closing(self.db.cursor()) as cursor:
            yield cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        """ Scores the input DataFrame using cached values, scoring any missing ones and adding them to the cache. """
        pta.validate.columns(inp, includes=[self.group, self.key])

        to_score_idxs = []
        to_score_map = {}

        inp = inp.reset_index(drop=True)
        values = pd.Series(index=inp.index, dtype=float)

        # First pass: load what we can from cache
        for group_key, group in inp.groupby(self.group):
            placeholder = ', '.join(['?'] * len(group))
            key2idxs = defaultdict(list)
            for idx, key in zip(group.index, group[self.key]):
                key2idxs[key].append(idx)
            with self._cursor() as cursor:
                cursor.execute(f'SELECT key, value FROM cache WHERE [group]=? AND key IN ({placeholder})',
                    [group_key] + group[self.key].tolist())
                for key, score in cursor.fetchall():
                    for idx in key2idxs[key]:
                        values[idx] = score
                    del key2idxs[key]
            for key, idxs in key2idxs.items():
                to_score_idxs.extend(idxs)
                to_score_map[group_key, key] = idxs

        # Second pass: score the missing ones and add to cache
        if to_score_idxs:
            if self.scorer is None:
                raise LookupError('values missing from cache, but no scorer provided')
            scored = self.scorer(inp.loc[to_score_idxs])
            records = scored[[self.group, self.key, self.value]]
            with closing(self.db.cursor()) as cursor:
                cursor.executemany('INSERT INTO cache ([group], key, value) VALUES (?, ?, ?)', records.itertuples(index=False))
                self.db.commit()
            for group, key, score in records.itertuples(index=False):
                for idx in to_score_map[group, key]:
                    values[idx] = score

        results = inp.assign(**{self.value: values})
        if self.value == 'score':
            pt.model.add_ranks(results)
        if self.verbose:
            print(f"{self}: {len(inp)-len(to_score_idxs)} hit(s), {len(to_score_idxs)} miss(es)")
        return results

    def merge_from(self, other: 'Sqlite3ScorerCache'):
        """ Merges the cached values from another Sqlite3ScorerCache instance into this one.

        Any keys that appear in both ``self`` and ``other`` will be replaced with the value from ``other``.
        """
        count = 0
        with self._cursor() as insert_cursor, other._cursor() as select_cursor:
            select_cursor.execute('SELECT [group], key, value FROM cache')
            while batch := select_cursor.fetchmany(10_000):
                count += len(batch)
                insert_cursor.executemany('INSERT OR REPLACE INTO cache ([group], key, value) VALUES (?, ?, ?)', batch)
            self.db.commit()
        if self.verbose:
            print(f"merged {count} records from {other} into {self}")

    def __repr__(self):
        return f'Sqlite3ScorerCache({str(self.path)!r}, {self.scorer!r}, group={self.group!r}, key={self.key!r})'


@deprecated(version='0.2.0', reason='ScorerCache will be switched from the dense `Hdf5ScorerCache` implementation to '
                                    'the sparse `Sqlite3ScorerCache` in a future version, which may break '
                                    'functionality that relies on it being a dense cache. Switch to DenseScorerCache '
                                    'to resolve this warning.')
class DeprecatedHdf5ScorerCache(Hdf5ScorerCache):
    pass

# Default implementations
ScorerCache = DeprecatedHdf5ScorerCache
DenseScorerCache = Hdf5ScorerCache
SparseScorerCache = Sqlite3ScorerCache
