import request from "supertest";
const jira = process.env["JIRA_BASEURL"] || "http://jira:8080/jira";
const adminPassword = process.env["JIRA_ADMIN_PWD"] || "admin";

test("Jira REST API returns a specific issue", async () =>
  await request(jira)
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

test("Jira REST API can create a ticket", async () =>
  await request(jira)
    .post("/rest/api/2/issue")
    .auth("admin", adminPassword)
    .set("Content-Type", "application/json")
    .send({
      fields: {
        project: { key: "KT" },
        summary: "New ticket" + Date.now(),
        issuetype: { name: "Task" },
      },
    })
    .expect(201));

test("JQL search returns issues assigned to admin", async () =>
  await request(jira)
    .get("/rest/api/2/search?jql=assignee=admin")
    .auth("admin", adminPassword)
    .set("Accept", "application/json")
    .expect("Content-Type", /json/)
    .expect(200)
    .then((resp) => {
      expect(resp.body.total).toEqual(16);
    }));

describe("Issue transitions", () => {
  let currentTransitionId: number;
  let targetTransitionId: number;
  // First we need to get transition IDs from a different API
  beforeAll(async () => {
    const transitions = await request(jira)
      .get("/rest/api/2/issue/KT-10/transitions")
      .auth("admin", adminPassword)
      .set("Accept", "application/json")
      .expect("Content-Type", /json/)
      .expect(200)
      .then((resp) => {
        return resp.body.transitions;
      });
    currentTransitionId = transitions.find((i: any) => i.name == "Done").id;
    targetTransitionId = transitions.find((i: any) => i.name == "In Progress")
      .id;
  });

  test("Transition issue from Done to In Progress", async () => {
    await request(jira)
      .post("/rest/api/2/issue/KT-10/transitions")
      .auth("admin", adminPassword)
      .set("Content-Type", "application/json")
      .send({
        transition: { id: targetTransitionId },
      })
      .expect(204);
  });

  // Move the issue back to Done so the test is idempotence
  afterAll(async () => {
    await request(jira)
      .post("/rest/api/2/issue/KT-10/transitions")
      .auth("admin", adminPassword)
      .set("Content-Type", "application/json")
      .send({
        transition: { id: currentTransitionId },
      })
      .expect(204);
  });
  // Move the issue back to Done
});
