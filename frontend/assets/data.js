export const ROLE_OPTIONS = [
  { label: 'Core Team', value: 'core_team' },
  { label: 'Intern', value: 'intern' },
  { label: 'Core Volunteer', value: 'core_volunteer' }
]

export const GENDER_OPTIONS = ['M', 'F']

export default { ROLE_OPTIONS, GENDER_OPTIONS }

export const LIST_QUERY_PATHS = {
  staffs: require('./../graphql/staff/GetAllStaff.graphql')
}

export const TABLE_HEADERS = {
  staffs: [
    { text: 'Name', value: 'name', align: 'start' },
    { text: 'Date Joined', value: 'date_joined' },
    { text: 'Profession', value: 'profession' },
    { text: 'Speech Therapist', value: 'is_speech_therapist' },
    { text: 'Projects Involved', value: '' },
    { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
  ]
}
