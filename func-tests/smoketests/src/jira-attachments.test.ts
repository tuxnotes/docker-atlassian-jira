import request from "supertest";
import fs from "fs";
const jira = process.env["JIRA_BASEURL"] || "http://jira:8080/jira";
const adminPassword = process.env["JIRA_ADMIN_PWD"] || "admin";

describe("Jira attachments", () => {
  const filename = "mynewfile3.txt";
  let attachments: number;

  beforeAll(() => {
    fs.writeFileSync(filename, "Hello content!");
  });

  test("Upload a new attachment to an issue", async () => {
    await request(jira)
      .get("/rest/api/2/issue/KT-5")
      .auth("admin", adminPassword)
      .set("Accept", "application/json")
      .expect("Content-Type", /json/)
      .expect(200)
      .then((resp) => {
        attachments = resp.body.fields.attachment.length;
      });

    await request(jira)
      .post("/rest/api/2/issue/KT-5/attachments")
      .auth("admin", adminPassword)
      .type("form")
      .set("X-Atlassian-Token", "no-check")
      .attach("file", filename)
      .expect("Content-Type", /json/)
      .expect(200);

    await request(jira)
      .get("/rest/api/2/issue/KT-5")
      .auth("admin", adminPassword)
      .set("Accept", "application/json")
      .expect("Content-Type", /json/)
      .expect(200)
      .then((resp) => {
        expect(resp.body.fields.attachment).toHaveLength(attachments + 1);
      });
  });

  afterAll(() => {
    fs.unlinkSync(filename);
  });
});
