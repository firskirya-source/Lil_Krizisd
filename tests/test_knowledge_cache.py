import json
import tempfile
import unittest
from unittest.mock import patch
from land_assistant.legal.knowledge import Knowledge
from test_legal_knowledge import make_library


class KnowledgeCacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=make_library(self.tmp.name)

    def test_repeated_reads_build_corpus_once(self):
        k=Knowledge(self.root,demo=True)
        with patch.object(Knowledge,'_build_fragments',wraps=k._build_fragments) as build:
            ids=[f['id'] for f in k.search('образование участка')]
            for fid in ids*3:k.read(fid)
            self.assertEqual(build.call_count,1)

    def test_edit_manifest_or_file_rebuilds_and_old_id_is_rejected(self):
        k=Knowledge(self.root,demo=True);fid=k.search('образование')[0]['id']
        k.read(fid)
        manifest=self.root/'laws/manifest.json';data=json.loads(manifest.read_text());data['documents'][0]['valid_until']='2000-01-01';manifest.write_text(json.dumps(data))
        with self.assertRaises(ValueError):k.read(fid)  # expired: must not be served from cache

    def test_unsafe_path_still_fails_after_cache_is_warm(self):
        k=Knowledge(self.root,demo=True);k.search('образование')
        manifest=self.root/'laws/manifest.json';data=json.loads(manifest.read_text());data['documents'][0]['path']='../../.env';manifest.write_text(json.dumps(data))
        with self.assertRaises(ValueError):k.search('образование')

    def test_returned_fragment_cannot_corrupt_cache(self):
        k=Knowledge(self.root,demo=True);fid=k.search('образование')[0]['id']
        k.read(fid)['text']='tampered'
        self.assertNotEqual(k.read(fid)['text'],'tampered')


if __name__=='__main__':
    unittest.main()
