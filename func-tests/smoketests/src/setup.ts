const superagent = require('superagent');
require('superagent-retry-delay')(superagent);

const request = require('supertest');

import { adminPassword, jiraBaseUrl } from "./config";

module.exports = async () => {
  console.log("Trigger issue re-index via Jira REST API")
  await request(jiraBaseUrl)
    .post("/rest/api/2/reindex")
    .query({ type: "FOREGROUND" })
    .auth("admin", adminPassword)
    .set("Content-Type", "application/json")
    .expect(202);
  
  await request(jiraBaseUrl)
    .get("/rest/api/2/reindex/progress")
    .auth("admin", adminPassword)
    .retry(5, 3000, [503])
    .expect(200);
};
