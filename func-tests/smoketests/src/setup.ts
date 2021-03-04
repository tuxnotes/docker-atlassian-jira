import request from "supertest";
import poll from "@jcoreio/poll";
import { adminPassword, jiraBaseUrl, indexingTimeout } from "./config";

module.exports = async () => {
  // This can be used for a common setup - e.g. indexing (but Jira indexes after startup and upgrade)

  console.log("");
  console.log('_.~"~._.~"~._.~"~._.~"~._');
  console.log(" Jira Docker smoke tests");
  console.log('_.~"~._.~"~._.~"~._.~"~._');

  console.log("Trigger issue re-index via Jira REST API");
  await request(jiraBaseUrl)
    .post("/rest/api/2/reindex")
    .query({ type: "FOREGROUND" })
    .auth("admin", adminPassword)
    .set("Content-Type", "application/json")
    .expect(202);

  // Jira returns 503 HTTP code for a short period while reindexing is triggered
  await poll(() => request(jiraBaseUrl).get("/rest/api/2/index/summary"), 500)
    .until((error, result) => result.status !== 503)
    .timeout(indexingTimeout)
    .then(() => console.log("Instance is responding now"));
};
