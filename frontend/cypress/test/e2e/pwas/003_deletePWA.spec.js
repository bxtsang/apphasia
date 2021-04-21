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

  it('Delete PWA', () => {
    cy.get('[data-cy=cy-listing-search-input]').type(PWA_001.name)

    cy.get('.v-data-table__wrapper')
      .find('tr')
      .should('contain', PWA_001.name)
      .should('contain', PWA_001.contact)
      .should('contain', PWA_001.status).click({multiple: true})
    
    cy.url().should('include', '/pwas?id=')

    cy.get('[data-cy=cy-edit-button]').click()

    cy.get('[data-cy=cy-delete-button]').click()

    cy.get('[data-cy=cy-confirm-delete-button]').click()

    cy.get('[data-cy=cy-notification-snackbar]').contains('Pwa successfully deleted')
  })
})