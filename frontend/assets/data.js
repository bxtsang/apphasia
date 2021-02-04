export const ROLE_OPTIONS = [
  { label: 'Core Team', value: 'core_team' },
  { label: 'Intern', value: 'intern' },
  { label: 'Core Volunteer', value: 'core_volunteer' }
]

export const GENDER_OPTIONS = ['M', 'F']

export const INPUT_VALIDATION = {
  role: {
    required: v => !!v || 'Role is required'
  },
  name: {
    required: v => !!v || 'Fullname is required'
  },
  dob: {
    required: v => !!v || 'Date of Birth is required'
  },
  contact: {
    required: v => !!v || 'Contact Number is required',
    valid: v => /(6|8|9)\d{7}/g.test(v) || 'Not a valid Contact Number'
  },
  gender: {
    required: v => !!v || 'Gender is required'
  },
  email: {
    required: v => !!v || 'E-mail is required',
    valid: v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
  },
  address: {
    required: v => !!v || 'Home Address is required'
  },
  profession: {
    required: v => !!v || 'Profession is required'
  },
  dateJoined: {
    required: v => !!v || 'Date Joined is required'
  },
  languages: {
    required: v => v.length > 0 || 'Language is required'
  },
  project_interest: {
    required: v => v.length > 0 || 'One Programme is required'
  },
  consent: {
    required: v => v != null || 'Consent is required'
  },
  multi_profession: {
    required: v => v.length > 0 || 'Profession is required'
  },
  wheelchair: {
    required: v => v != null || 'Wheelchair usage is required'
  }
}

export const LIST_QUERY_PATHS = {
  staffs: require('./../graphql/staff/GetAllStaff.graphql'),
  volunteers: require('./../graphql/volunteer/GetAllVol.graphql'),
  pwas: require('./../graphql/pwa/GetAllPWA.graphql')
}

export const TABLE_HEADERS = {
  staffs: [
    { text: 'Name', value: 'name', align: 'start' },
    { text: 'Date Joined', value: 'date_joined' },
    { text: 'Profession', value: 'profession' },
    { text: 'Speech Therapist', value: 'is_speech_therapist' },
    { text: 'Projects Involved', value: '' },
    { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
  ],
  volunteers: [
    { text: 'Name', value: 'name', align: 'start' },
    { text: 'Gender', value: 'gender' },
    { text: 'Date of Birth', value: 'dob' },
    { text: 'Profession', value: 'profession' },
    { text: 'Programmes Interest', value: 'project_vols' },
    { text: 'Speech Therapist?', value: 'is_speech_therapist' },
    { text: 'Status', value: 'status' },
    { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
  ],
  pwas: [
    { text: 'Name', value: 'general_info.name', align: 'start' },
    { text: 'Communication Difficulties', value: 'comm_diff' },
    { text: 'Programmes Involved In', value: 'projects' },
    { text: 'NOK', value: 'nok' },
    { text: 'Languages understand/speak', value: 'languages' },
    { text: 'Status', value: 'contact_status' },
    { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
  ]
}

// VOLUNTEER DATA

export const VOLUNTEER_STATUS = {
  Approved: {
    chipColor: 'success'
  },
  Pending_Approval: {
    chipColor: 'warning'
  },
  Rejected: {
    chipColor: 'error'
  },
  KIV: {
    chipColor: 'error'
  }
}

export const CONTACT_STATUS = {
  Contacted: {
    chipColor: 'success'
  },
  'Contacted but no response': {
    chipColor: 'warning'
  },
  'Not Contacted': {
    chipColor: 'error'
  }
}

export const COMMON_PROFESSIONS = [
  'Speech and Langauge Therapist (SLT)',
  'Music Therapist',
  'Occupational Therapist',
  'Social Worker',
  'Healthcare professional (but none of the above)',
  'SLT Student',
  'Student (but not in the field of speech therapy)'
]

export const EDIT_RESOURCE_PERMISSIONS = {
  staffs: ['core_team'],
  volunteers: ['core_team', 'intern'],
  pwas: ['core_team', 'intern']
}
