
import supertest from 'supertest'

const jira = "http://jira:8080/jira"

describe('Jira status endpoint', () => {
  it('responds with RUNNING', async () => {
    supertest(jira)
      .get('/status')
      .set('Accept', 'application/json')
      .expect('Content-Type', /json/)
      .expect(200)
      .then(resp => {
          expect(resp.body).toMatchObject({state: "RUNNING"})
      })
  })
})
