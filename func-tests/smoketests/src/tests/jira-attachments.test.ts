import request from "supertest";
import fs from "fs";
import { adminPassword, jiraBaseUrl } from "../config";

describe("Jira attachments", () => {
  const filename = "mynewfile3.txt";
  let attachments: number;

  beforeAll(() => {
    fs.writeFileSync(filename, "Hello content!");
  });

  test("Upload a new attachment to an issue", async () => {
    await request(jiraBaseUrl)
      .get("/rest/api/2/issue/KT-5")
      .auth("admin", adminPassword)
      .set("Accept", "application/json")
      .expect(200)
      .expect("Content-Type", /json/)
      .then((resp) => {
        attachments = resp.body.fields.attachment.length;
      });

    await request(jiraBaseUrl)
      .post("/rest/api/2/issue/KT-5/attachments")
      .auth("admin", adminPassword)
      .type("form")
      .set("X-Atlassian-Token", "no-check")
      .attach("file", filename)
      .expect("Content-Type", /json/)
      .expect(200);

    await request(jiraBaseUrl)
      .get("/rest/api/2/issue/KT-5")
      .auth("admin", adminPassword)
      .set("Accept", "application/json")
      .expect("Content-Type", /json/)
      .expect(200)
      .retry(5)
      .then((resp) => {
        expect(resp.body.fields.attachment).toHaveLength(attachments + 1);
      });
  });

  afterAll(() => {
    fs.unlinkSync(filename);
  });
});
