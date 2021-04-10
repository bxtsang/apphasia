
import { PWA_001 } from './../../../fixtures/PWA.js'
describe('Login to Apphasia', () =>  {
  
  
  beforeEach(() => {
    cy.visit('/')
    cy.get('[data-cy=cy-login-email-input]').type('arixgg@gmail.com')
    cy.get('[data-cy=cy-login-password-input]').type('Password1!')
    cy.get('[data-cy=cy-login-submit-input]').click()
    cy.url().should('not.include', '/login')
    cy.visit('/pwas')
    cy.url().should('include', '/pwas')
  })

  it('Add New PWA', () => {
    cy.get('[data-cy=cy-add-resource-btn]').click()
    cy.get('[data-cy=cy-form-name-input]').type(PWA_001.name)
  })

})