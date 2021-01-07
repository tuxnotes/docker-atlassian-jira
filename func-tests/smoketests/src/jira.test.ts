
import supertest from 'supertest'

let jira = "http://jira:8080/jira"

describe('Get status', () => {
  it('responds with OK', async (done) => {
    supertest(jira)
      .get('/status')
      .set('Accept', 'application/json')
      .expect('Content-Type', /json/)
      .expect(200, done)
  });
});
