describe('Login to Apphasia', () =>  {

    beforeEach(() => {
        cy.visit('/')
    })

    it('Middleware Redirecting to /login', () => {
        cy.url().should('include', '/login')
    })

    it('Check for Missing Email & Password', () => {
        cy.get('[data-cy=cy-login-submit-input]').click()
        cy.get('.v-text-field__details').eq(0).contains('E-mail is required')
        cy.get('.v-text-field__details').eq(1).contains('Password is required')
    })

    it('Check for Invalid Email', () => {

    })

    it('Successful Login'), () => {

    }

})