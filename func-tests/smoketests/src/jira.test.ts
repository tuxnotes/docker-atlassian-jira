import request from "supertest";
const jira = process.env["JIRA_BASEURL"] || "http://jira:8080/jira";
const adminPassword = process.env["JIRA_ADMIN_PWD"] || "admin";

describe("Jira status endpoint", () => {
  it("responds with RUNNING", () =>
    request(jira)
      .get("/status")
      .set("Accept", "application/json")
      .expect("Content-Type", /json/)
      .expect(200)
      .then((resp) => {
        expect(resp.body).toMatchObject({ state: "RUNNING" });
      }));
});

describe("Jira REST API", () => {
  it("returns a specific issue", () =>
    request(jira)
      .get("/rest/agile/1.0/issue/KT-1")
      .auth("admin", adminPassword)
      .set("Accept", "application/json")
      .expect("Content-Type", /json/)
      .expect(200)
      .then((resp) => {
        expect(resp.body.fields).toEqual(
          expect.objectContaining({
            summary:
              "Kanban cards represent work items >> Click the \"KT-1\" link at the top of this card to show the Detail view - there's more on Kanban in the 'Description' section",
          })
        );
      }));
});
