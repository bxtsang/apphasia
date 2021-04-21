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
        cy.get('[data-cy=cy-login-email-input]').type('usernameExample')
        cy.get('.v-text-field__details').eq(0).contains('E-mail must be valid')

        cy.get('.v-text-field__details').eq(1).should('not.have.value', 'Password is required')
        cy.get('[data-cy=cy-login-submit-input]').click()
        cy.get('.v-text-field__details').eq(1).contains('Password is required')
    })


    it('Check for Unsuccessful Login', () => {
        cy.get('[data-cy=cy-login-email-input]').type('doesNotExist@example.com')
        cy.get('[data-cy=cy-login-password-input]').type('password')
        
        cy.get('[data-cy=cy-notification-snackbar]').should('have.value', '')
        cy.get('[data-cy=cy-login-submit-input]').click()
        cy.get('[data-cy=cy-notification-snackbar]').contains('Incorrect username or password')

        cy.get('[data-cy=cy-login-email-input]').should('have.value', '')
        cy.get('[data-cy=cy-login-password-input]').should('have.value', '')
    })

    it('Check for Successful Login', () => {
        cy.get('[data-cy=cy-login-email-input]').type('arixgg@gmail.com')
        cy.get('[data-cy=cy-login-password-input]').type('Password1!')

        cy.get('[data-cy=cy-login-submit-input]').click()
        cy.url().should('not.include', '/login')
    })

})