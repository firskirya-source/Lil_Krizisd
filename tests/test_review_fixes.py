import asyncio
import tempfile
import unittest
from unittest.mock import patch
from land_assistant.legal import speech
from land_assistant.legal.model import DemoModel
from land_assistant.legal.pipeline import LegalPipeline
from test_legal_knowledge import make_library


class ReviewFixTests(unittest.TestCase):
    def test_bad_known_fields_from_classifier_do_not_fail_request(self):
        class NoisyModel(DemoModel):
            async def classify(self,question,intake=None,**kw):
                plan=await super().classify(question,intake,**kw)
                return {**plan,'known_fields':{'amount':500000,'region':None,'situation':['x'],'rights':' право собственности ','cadastral_number':'1'*5000}}
        with tempfile.TemporaryDirectory() as tmp:
            result=asyncio.run(LegalPipeline(make_library(tmp),NoisyModel(),demo=True).run('Образование участка',{'situation':'Участок','goal':'Порядок образования'}))
            self.assertNotEqual(result['diagnostics'].get('code'),'invalid_plan')
            self.assertIn(result['status'],('answered','partial_answer'))

    def test_real_source_error_is_reported_instead_of_empty_search(self):
        class Pipeline(LegalPipeline):
            async def context_for_task(self,task,**kw):return {'prompt':'','fragments':[],'trace':[],'source_errors':[]}
            async def fallback_context(self,task,**kw):
                return {'prompt':'','fragments':[],'trace':[],'source_errors':['search_no_candidates','source_rate_limit']}
        with tempfile.TemporaryDirectory() as tmp:
            result=asyncio.run(Pipeline(make_library(tmp),DemoModel(),demo=True).run('Образование участка',{'situation':'Участок','goal':'Порядок образования'}))
            self.assertEqual(result['status'],'error')
            self.assertEqual(result['diagnostics']['code'],'source_rate_limit')

    def test_speech_interpreter_path_matches_platform(self):
        with patch('land_assistant.legal.speech.os.name','nt'):
            self.assertEqual(speech.interpreter().parts[-2:],('Scripts','python.exe'))
        with patch('land_assistant.legal.speech.os.name','posix'):
            self.assertEqual(speech.interpreter().parts[-2:],('bin','python'))


if __name__=='__main__':
    unittest.main()
