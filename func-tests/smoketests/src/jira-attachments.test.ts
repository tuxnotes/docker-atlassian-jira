import request from "supertest";
const jira = process.env["JIRA_BASEURL"] || "http://jira:8080/jira";
const adminPassword = process.env["JIRA_ADMIN_PWD"] || "admin";

test("We can upload an attachment to Jira ticket", async () => {
  let attachments: number;
  await request(jira)
    .get("/rest/agile/1.0/issue/KT-5")
    .auth("admin", adminPassword)
    .set("Accept", "application/json")
    .expect("Content-Type", /json/)
    .expect(200)
    .then((resp) => {
      attachments = resp.body.fields.attachment.length
    });

  await request(jira)
    .post("/rest/api/2/issue/KT-5/attachments")
    .auth("admin", adminPassword)
    .type("form")
    .set("X-Atlassian-Token", "no-check")
    .attach('file', '/tmp/adobegc.log')
    .expect("Content-Type", /json/)
    .expect(200)

    await request(jira)
    .get("/rest/agile/1.0/issue/KT-5")
    .auth("admin", adminPassword)
    .set("Accept", "application/json")
    .expect("Content-Type", /json/)
    .expect(200)
    .then((resp) => {
      expect(resp.body.fields.attachment).toHaveLength(attachments + 1);
    });
});
