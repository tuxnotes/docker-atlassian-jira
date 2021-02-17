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
      expect(plugins).toHaveLength(280);
      plugins.map((plugin: any) =>
        expect(plugin).toHaveProperty("enabled", true)
      );
    });
});
