export const ROLE_OPTIONS = [
  { label: 'Core Team', value: 'core_team' },
  { label: 'Intern', value: 'intern' },
  { label: 'Core Volunteer', value: 'core_volunteer' }
]

export const GENDER_OPTIONS = ['M', 'F']

export const COMM_DIFF_OPTIONS = [
  'Speaking',
  'Understanding what others are saying',
  'Reading',
  'Writing',
  'Using numbers'
]

export const PWA_CONTACT_STATUS_OPTIONS = [
  'Not Contacted',
  'Contacted but no response',
  'Contacted'
]

export const PWA_PREFFERED_CONTACTED_OPTIONS = [
  'Whatsapp',
  'Email',
  'SMS',
  'Call'
]

export const INPUT_VALIDATION = {
  role: {
    required: v => !!v || 'Role is required'
  },
  name: {
    required: v => !!v || 'Full Name is required'
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
  },
  comm_diff: {
    required: v => v.length > 0 || 'One Communication Difficulty is required'
  },
  pref_comm: {
    required: v => !!v || 'One Mode of Communication is required'
  }
}

export const LIST_QUERY_PATHS = {
  staffs: require('./../graphql/staff/GetAllStaff.graphql'),
  volunteers: require('./../graphql/volunteer/GetAllVol.graphql'),
  pwas: require('./../graphql/pwa/GetAllPWA.graphql'),
  projects: require('./../graphql/project/GetAllProject.graphql'),
  events: require('./../graphql/event/GetAllEvent.graphql'),
  timeline: require('./../graphql/dashboard/GetTimelineEvents.graphql'),
  notification: {
    unread: require('./../graphql/notifications/GetNotificationsOfStaffInitial.graphql'),
    unreadSubscription: require('./../graphql/notifications/GetNotificationsOfStaff.graphql'),
    read: require('./../graphql/notifications/GetReadNotificationsOfStaff.graphql')
  }
}

export const TABLE_HEADERS = {
  staffs: [
    { text: 'Name', value: 'name', align: 'start' },
    { text: 'Date Joined', value: 'date_joined' },
    { text: 'Profession', value: 'profession' },
    { text: 'Speech Therapist', value: 'is_speech_therapist' },
    { text: 'Projects Involved', value: 'projects_in', sortable: false },
    { text: '', value: 'actions', sortable: false, align: 'end' }
  ],
  volunteers: [
    { text: 'Name', value: 'general_info.name', align: 'start' },
    { text: 'Gender', value: 'general_info.gender' },
    { text: 'Date of Birth', value: 'general_info.dob' },
    { text: 'Profession', value: 'profession' },
    { text: 'Programmes Interested  ', value: 'project_vols', sortable: false },
    { text: 'Speech Therapist', value: 'is_speech_therapist' },
    { text: 'Status', value: 'status' },
    { text: '', value: 'actions', sortable: false, align: 'end' }
  ],
  pwas: [
    { text: 'Name', value: 'general_info.name', align: 'start' },
    { text: 'Communication Difficulties', value: 'comm_diff', sortable: false },
    { text: 'Programmes Involved', value: 'projects', sortable: false },
    { text: 'NOK', value: 'nok', sortable: false },
    { text: 'Languages understand/speak', value: 'languages', sortable: false },
    { text: 'Status', value: 'contact_status' },
    { text: '', value: 'actions', sortable: false, align: 'end' }
  ],
  projects: [
    { text: 'Project Name', value: 'title' },
    { text: 'Upcoming DateTime', value: 'upcoming_date' },
    { text: 'Recurring?', value: 'is_recurring' },
    { text: 'Staff Involved', value: 'staffs', sortable: false },
    { text: 'Notes', value: 'description' },
    { text: '', value: 'actions', sortable: false, align: 'end' }
  ],
  events: [
    { text: 'Name', value: 'name' },
    { text: 'Date', value: 'date' },
    { text: 'Time', value: 'event_time' },
    { text: '', value: 'actions', sortable: false, align: 'end' }
  ]
}

// VOLUNTEER DATA

export const VOLUNTEER_STATUS = {
  Approved: {
    chipColor: 'success'
  },
  'Pending Approval': {
    chipColor: 'warning'
  },
  Rejected: {
    chipColor: 'error'
  },
  KIV: {
    chipColor: 'warning'
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

export const VOLUNTEER_TYPES = {
  Befriender: 'Befriender',
  Project_Volunteer: 'Project Volunteer'
}

export const EDIT_RESOURCE_PERMISSIONS = {
  staffs: ['admin', 'core_team'],
  volunteers: ['admin', 'core_team', 'intern'],
  pwas: ['admin', 'core_team', 'intern'],
  projects: ['admin', 'core_team', 'intern'],
  events: ['admin', 'core_team', 'intern']
}

// EVENT DATA
export const DAY = [
  { value: 0, text: 'Monday' },
  { value: 1, text: 'Tuesday' },
  { value: 2, text: 'Wednesday' },
  { value: 3, text: 'Thursday' },
  { value: 4, text: 'Friday' },
  { value: 5, text: 'Saturday' },
  { value: 6, text: 'Sunday' }
]

export const WEEK = [
  { value: 1, text: '1st' },
  { value: 2, text: '2nd' },
  { value: 3, text: '3rd' },
  { value: 4, text: '4th' }
]
