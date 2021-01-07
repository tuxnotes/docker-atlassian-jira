
import supertest from 'supertest'

let jira = "http://jira:8080/jira"

describe('Get status', () => {
  it('Responds with RUNNING', async () => {
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
