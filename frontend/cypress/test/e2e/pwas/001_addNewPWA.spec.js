describe('Login to Apphasia', () =>  {

  beforeEach(() => {
    cy.visit('/')
    cy.get('[data-cy=cy-login-email-input]').type('arixgg@gmail.com')
    cy.get('[data-cy=cy-login-password-input]').type('Password1!')
    cy.get('[data-cy=cy-login-submit-input]').click()
    cy.url().should('not.include', '/login')
    cy.visit('/pwas')
  })

  it('Add New PWA', () => {
    cy.url().should('include', '/pwas')
  })

})