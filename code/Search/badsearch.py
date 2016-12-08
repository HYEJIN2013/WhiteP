from elasticsearch import Elasticsearch, TransportError
import json
client = Elasticsearch()
try:
    client.search(body={'foo': 'bar'})
except TransportError as ex:
    print(ex.error)
    print(json.dumps(ex.info, indent=2))
    
"""
search_phase_execution_exception
{
  "error": {
    "type": "search_phase_execution_exception",
    "root_cause": [
      {
        "line": 1,
        "type": "search_parse_exception",
        "col": 2,
        "reason": "failed to parse search source. unknown search element [foo]"
      }
    ],
    "reason": "all shards failed",
    "grouped": true,
    "failed_shards": [
      {
        "index": ".kibana",
        "shard": 0,
        "node": "63sIQImaQe-7sPNoMqLORw",
        "reason": {
          "line": 1,
          "type": "search_parse_exception",
          "col": 2,
          "reason": "failed to parse search source. unknown search element [foo]"
        }
      }
    ],
    "phase": "query"
  },
  "status": 400
}
"""
