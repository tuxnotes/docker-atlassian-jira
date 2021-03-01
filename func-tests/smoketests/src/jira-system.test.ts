import request from "supertest";
const jira = process.env["JIRA_BASEURL"] || "http://jira:8080/jira";
const adminPassword = process.env["JIRA_ADMIN_PWD"] || "admin";

test("Jira status endpoint responds with RUNNING", async () =>
  await request(jira)
    .get("/status")
    .set("Accept", "application/json")
    .expect("Content-Type", /json/)
    .expect(200)
    .then((resp) => {
      expect(resp.body).toMatchObject({ state: "RUNNING" });
    }));

test("Verify that all plugins are enabled", async () => {
  await request(jira)
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
  await request(jira)
    .get("/rest/api/2/index/summary")
    .auth("admin", adminPassword)
    .expect("Content-Type", /json/)
    .expect(200)
    .then((resp) => {
      expect(resp.body.issueIndex.indexReadable).toEqual(true);
      const countInDatabase = resp.body.issueIndex.countInDatabase;
      expect(countInDatabase).toBeGreaterThan(0);
      expect(resp.body.issueIndex.countInIndex).toEqual(countInDatabase);
    });
});