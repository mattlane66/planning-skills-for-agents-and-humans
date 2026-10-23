import assert from 'node:assert/strict';
import { startBridge, validateRequest, validateResponse, buildPrompt, runModel } from './agent-bridge.mjs';

const base = [
  'version: breadboard/v1',
  'P1 | place | Request | Enter request | app',
  ''
].join('\n');
const input = {
  project_id: 'project-unit-test', option_id: 'A',
  base_dsl: base, instruction: 'Add a submit action.',
  context: {name:'Test',problem:['People need to submit a request'],outcome:['User sees confirmation'],requirements:['R1: submit'],appetite:'2 weeks',cut:'No admin dashboard'}
};
const expected = validateRequest(input);
const patch = {
  kind:'BreadboardPatch',schema_version:1,project_id:input.project_id,option_id:'A',base_dsl:base,
  operations:[
    {op:'add_node',node:{id:'U1',kind:'ui',title:'Submit',detail:'Send request',system:'app',parent:'P1'}},
    {op:'add_edge',from:'P1',to:'U1',kind:'control'}
  ]
};
assert.equal(validateResponse(patch,expected).revision.changes.length,2);
assert.equal(validateRequest({...input,option_id:'CURRENT'}).option_id,'CURRENT');
assert.match(buildPrompt(expected),/EXACT CANONICAL BASE_DSL/);
assert.throws(()=>validateRequest({...input,base_dsl:'P1 | place | legacy | | app\n'}),/fixed-language/);
assert.throws(()=>validateRequest({...input,instruction:'x'.repeat(2400)}),/2200/);
assert.throws(()=>validateResponse({...patch,option_id:'B'},expected),/different/);
assert.throws(()=>validateResponse({...patch,operations:[{op:'add_node',node:{id:'X1',kind:'magic',title:'A',detail:'',system:'app'}}]},expected),/Invalid kind/);
assert.throws(()=>validateResponse({...patch,base_dsl:base+'# stale\n'},expected),/Stale/);

let invocations=0;
const server=await startBridge({port:0,runner:async request=>{
  invocations++;
  assert.equal(request.option_id,'A');
  return patch;
}});
try {
  const htmlResponse=await fetch(server.url);
  assert.equal(htmlResponse.status,200);
  const html=await htmlResponse.text();
  const token=html.match(/__SHAPING_AGENT_SESSION="([a-f0-9]{64})"/)?.[1];
  assert.ok(token,'local page must contain an unguessable per-process secret');
  assert.match(html,/Shape with AI/);
  assert.equal(htmlResponse.headers.get('x-frame-options'),'DENY');
  const origin=new URL(server.url).origin;
  const post=(body,headers={})=>fetch(server.url+'api/propose',{
    method:'POST',headers:{'Content-Type':'application/json','Origin':origin,'X-Shaping-Session':token,...headers},
    body:JSON.stringify(body)
  });
  const untrusted=await post(input,{'X-Shaping-Session':'wrong'});
  assert.equal(untrusted.status,403);
  const otherOrigin=await post(input,{'Origin':'https://evil.example'});
  assert.equal(otherOrigin.status,403);
  assert.equal(invocations,0,'no cross-site execution');
  const malformed=await post({...input,option_id:'../danger'});
  assert.equal(malformed.status,422);
  assert.equal(invocations,0,'invalid input must not invoke a model');
  const valid=await post(input);
  assert.equal(valid.status,200,await valid.clone().text());
  const proposal=await valid.json();
  assert.equal(proposal.change_count,2);
  assert.deepEqual(proposal.proposal,patch);
  assert.equal(invocations,1);
  const status=await fetch(server.url+'api/status');
  assert.equal((await status.json()).connected,true);
  const noRoute=await fetch(server.url+'../../etc/passwd');
  assert.equal(noRoute.status,404);
} finally { await server.close(); }

// Verify the model transport is tool-free and the API key never enters the prompt body.
const outputPayload={status:'completed',output:[{type:'message',content:[{type:'output_text',text:JSON.stringify(patch)}]}]};
let seenAPI;
const returned=await runModel(expected,{
  apiKey:'unit-test-secret',model:'gpt-6-astra',
  fetcher:async (url,init)=>{
    seenAPI={url,init};
    return {ok:true,status:200,text:async()=>JSON.stringify(outputPayload)};
  }
});
assert.deepEqual(returned,patch);
assert.equal(seenAPI.url,'https://api.openai.com/v1/responses');
assert.equal(seenAPI.init.headers.Authorization,'Bearer unit-test-secret');
const payload=JSON.parse(seenAPI.init.body);
assert.deepEqual(payload.tools,[]);
assert.equal(payload.tool_choice,'none');
assert.equal(payload.store,false);
assert.match(payload.input,/EXACT CANONICAL BASE_DSL/);
assert.ok(!seenAPI.init.body.includes('unit-test-secret'),'the API key must never enter the model prompt');
await assert.rejects(()=>runModel(expected,{apiKey:'',fetcher:async()=>{throw Error('should not call')}}),/OPENAI_API_KEY/);
await assert.rejects(()=>runModel(expected,{apiKey:'secret',fetcher:async()=>({ok:false,status:401})}),/HTTP 401/);
await assert.rejects(()=>runModel(expected,{apiKey:'secret',fetcher:async()=>({
 ok:true,status:200,text:async()=>JSON.stringify({...outputPayload,output:[]})
})}),/no usable JSON/);

console.log('Shaping local agent bridge: validated patch, tool-free model API, local origin/session boundary, no auto-write');
