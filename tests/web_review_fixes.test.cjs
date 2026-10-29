const {test}=require('node:test');
const assert=require('node:assert/strict');
const {publicResult}=require('../groundAndLaw/legal-api.js');

test('act named exactly as the server-built basis title is accepted regardless of case',()=>{
 const bases=[{title:'136-ФЗ от 25.10.2001 «Земельный кодекс Российской Федерации»',article:'Статья 11.8. Образование участка',explanation:'Порядок.'}];
 for(const answer of [
  'Порядок определяет Земельный кодекс Российской Федерации.',
  'Порядок определяет земельный кодекс российской федерации, статья 11.8.',
  'См. 136-ФЗ от 25.10.2001 «Земельный кодекс Российской Федерации».',
 ]){
  const result=publicResult({status:'answered',answer,legal_bases:bases});
  assert.equal(result.status,'answered',answer);
  assert.equal(result.answer,answer);
 }
});

test('unconfirmed articles and acts are still rejected next to a valid basis',()=>{
 const bases=[{title:'136-ФЗ от 25.10.2001 «Земельный кодекс Российской Федерации»',article:'Статья 11.8. Образование участка',explanation:'Порядок.'}];
 for(const answer of ['Подробнее в статье 99 Земельного кодекса.','Также см. Трудовой кодекс РФ.','См. https://example.org/law']){
  assert.equal(publicResult({status:'answered',answer,legal_bases:bases}).status,'error',answer);
 }
});
