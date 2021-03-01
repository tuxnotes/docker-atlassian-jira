import request from "supertest";
import { adminPassword, jiraBaseUrl } from "../config";

test("Jira status endpoint responds with RUNNING", async () =>
  await request(jiraBaseUrl)
    .get("/status")
    .set("Accept", "application/json")
    .expect("Content-Type", /json/)
    .expect(200)
    .then((resp) => {
      expect(resp.body).toMatchObject({ state: "RUNNING" });
    }));

test("Verify that all plugins are enabled", async () => {
  await request(jiraBaseUrl)
    .get("/rest/plugins/1.0/")
    .auth("admin", adminPassword)
    .expect("Content-Type", /json/)
    .expect(200)
    .then((resp) => {
      const plugins = resp.body.plugins;
      // we shouldn't rely on precise number of plugins as this is subject to change
      expect(plugins.length).toBeGreaterThan(200);
      // but all of the plugins should be enabled
      plugins.map((plugin: any) =>
        expect(plugin).toHaveProperty("enabled", true)
      );
    });
});

test("Verify that index is readable", async () => {

  await request(jiraBaseUrl)
    .get("/rest/api/2/index/summary")
    .auth("admin", adminPassword)
    .expect(200)
    .expect("Content-Type", /json/)
    .then((resp) => {
      expect(resp.body.issueIndex.indexReadable).toEqual(true);
      const countInDatabase = resp.body.issueIndex.countInDatabase;
      expect(countInDatabase).toBeGreaterThan(0);
      // expect(resp.body.issueIndex.countInIndex).toEqual(countInDatabase); // there are potential inconsistencies (N+1 problem)
      expect(resp.body.issueIndex.countInIndex).toBeGreaterThan(0);
    });
});
