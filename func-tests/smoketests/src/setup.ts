import request from "supertest";
import { adminPassword, jiraBaseUrl } from "./config";

module.exports = async () => {
  jest.setTimeout(60000);
  console.log("Trigger issue re-index via Jira REST API")
  await request(jiraBaseUrl)
    .post("/rest/api/2/reindex")
    .query({ type: "FOREGROUND" })
    .auth("admin", adminPassword)
    .set("Content-Type", "application/json")
    .expect(202);
};
