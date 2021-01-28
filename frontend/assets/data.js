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
  nric: {
    required: v => !!v || 'NRIC is required',
    valid: v => /^[STFG]\d{7}[A-Z]$/.test(v) || 'Not a valid NRIC'
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
  }
}

export const LIST_QUERY_PATHS = {
  staffs: require('./../graphql/staff/GetAllStaff.graphql'),
  volunteers: require('./../graphql/volunteer/GetAllVol.graphql')
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

export const VOLUNTEER_CHANNELS = {
  facebook: {
    text: 'Facebook'
  },
  instagram: {
    text: 'Instagram'
  },
  twitter: {
    text: 'Twitter'
  },
  linkedIn: {
    text: 'LinkedIn'
  },
  public_outreach: {
    text: 'Public Outreach'
  },
  workshops_or_talks: {
    text: 'From talks/workshops'
  },
  patients_or_caregivers: {
    text: 'From patients/caregivers'
  },
  school: {
    text: 'From my school/education institution'
  },
  other_volunteers: {
    text: 'From other volunteers'
  },
  radio: {
    text: 'Radio'
  },
  our_website: {
    text: 'Aphasia SG Website'
  },
  speech_therapist: {
    text: 'From a Speech Therapist'
  },
  other_healthcare_professionals: {
    text: 'From other healthcare professionals'
  },
  newspaper: {
    text: 'Newspaper'
  },
  hospital_advertisement: {
    text: 'Saw the advertisment in a hospital'
  },
  word_of_mouth: {
    text: 'Word of mouth'
  },
  social_care_centre: {
    text: 'Social care centre'
  },
  doctor: {
    text: 'Doctor'
  }
}
