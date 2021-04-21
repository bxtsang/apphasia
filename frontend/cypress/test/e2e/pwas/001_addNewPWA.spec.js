
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

    cy.get('[data-cy=cy-form-dob-input]').click()
    cy.get('[data-cy=cy-form-dob-picker] .v-date-picker-years li').contains(PWA_001.dob.split('-')[0]).click()
    cy.get('[data-cy=cy-form-dob-picker] .v-date-picker-table--month button').contains(PWA_001.dob.split('-')[1]).click()
    cy.get('[data-cy=cy-form-dob-picker] .v-date-picker-table--date button').contains(PWA_001.dob.split('-')[2]).click()

    cy.get('[data-cy=cy-form-contact-input]').type(PWA_001.contact)
    cy.get('[data-cy=cy-form-gender-input]').click()
    cy.get('[data-cy=cy-form-gender-input] .v-input__control .v-input__slot')
    .then(input => {
      cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(PWA_001.gender).click()
    })

    cy.get('[data-cy=cy-form-email-input]').type(PWA_001.email)
    cy.get('[data-cy=cy-form-address-input]').type(PWA_001.address)
    cy.get('[data-cy=cy-form-bio-input]').type(PWA_001.bio)

    cy.get('[data-cy=cy-form-wheelchair-input]').click()
    cy.get('[data-cy=cy-form-wheelchair-input] .v-input__control .v-input__slot')
    .then(input => {
      cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(PWA_001.wheelchair).click()
    })

    cy.get('[data-cy=cy-form-projects-input]').click()
    cy.get('[data-cy=cy-form-projects-input] .v-input__control .v-input__slot')
    .then(input => {
      PWA_001.projects_involved.map(project => cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(project).click())
    })

    cy.get('[data-cy=cy-form-comm-diff-input]').click()
    cy.get('[data-cy=cy-form-comm-diff-input] .v-input__control .v-input__slot')
    .then(input => {
      PWA_001.comm_diff.map(diff => cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(diff).click())
    })

    cy.get('[data-cy=cy-form-language-input]').click()
    cy.get('[data-cy=cy-form-language-input] .v-input__control .v-input__slot')
    .then(input => {
      PWA_001.languages.map(language => cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(language).click())
    })
    
    cy.get('[data-cy=cy-form-stroke-date-input]').click()
    cy.get('[data-cy=cy-form-stroke-date-picker] .v-date-picker-years li').contains(PWA_001.stroke_date.split('-')[0]).click()
    cy.get('[data-cy=cy-form-stroke-date-picker] .v-date-picker-table--month button').contains(PWA_001.stroke_date.split('-')[1]).click()
    cy.get('[data-cy=cy-form-stroke-date-picker] .v-date-picker-table--date button').contains(PWA_001.stroke_date.split('-')[2]).click()
  
    cy.get('[data-cy=cy-form-channel-input]').click()
    cy.get('[data-cy=cy-form-channel-input] .v-input__control .v-input__slot')
    .then(input => {
      cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(PWA_001.channel).click()
    })

    cy.get('[data-cy=cy-form-consent-input]').click()
    cy.get('[data-cy=cy-form-consent-input] .v-input__control .v-input__slot')
    .then(input => {
      cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(PWA_001.consent).click()
    })

    cy.get('[data-cy=cy-form-media-input]').click()
    cy.get('[data-cy=cy-form-media-input] .v-input__control .v-input__slot')
    .then(input => {
      cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(PWA_001.media).click()
    })

    cy.get('[data-cy=cy-form-media-engagement-input]').type(PWA_001.media_engagement)
    
    cy.get('[data-cy=cy-form-status-input]').click()
    cy.get('[data-cy=cy-form-status-input] .v-input__control .v-input__slot')
    .then(input => {
      cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(PWA_001.status).click()
    })

    cy.get('[data-cy=cy-form-comm-mode-input]').click()
    cy.get('[data-cy=cy-form-comm-mode-input] .v-input__control .v-input__slot')
    .then(input => {
      cy.get(`#${input.attr('aria-owns')} .v-list-item`).contains(PWA_001.comm_mode).click()
    })
    
    cy.get('[data-cy=cy-form-submit-pwa-input]').click()

    cy.get('[data-cy=cy-notification-snackbar]').contains('PWA successfully created')
  })
})