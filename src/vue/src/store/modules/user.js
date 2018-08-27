import Vue from 'vue'
import * as types from '../constants/mutation-types.js'
import connection from '@/api/connection.js'

const getters = {
    jwtAccess: state => state.jwtAccess,
    jwtRefresh: state => state.jwtRefresh,
    uID: state => state.uID,
    username: state => state.username,
    email: state => state.email,
    verifiedEmail: state => state.verifiedEmail,
    profilePicture: state => state.profilePicture,
    firstName: state => state.firstName,
    lastName: state => state.lastName,
    ltiID: state => state.ltiID,
    gradeNotifications: state => state.gradeNotifications,
    commentNotifications: state => state.commentNotifications,
    permissions: state => state.permissions,
    loggedIn: state => state.jwtAccess !== null,
    storePopulated: state => state.uID !== null
}

const mutations = {
    [types.LOGIN] (state, data) {
        state.jwtAccess = data.access
        state.jwtRefresh = data.refresh
    },
    [types.HYDRATE_USER] (state, data) {
        const userData = data.user_data
        const permissions = data.all_permissions

        state.uID = userData.uID
        state.username = userData.username
        state.email = userData.email
        state.verifiedEmail = userData.verified_email
        state.profilePicture = userData.picture
        state.firstName = userData.first_name
        state.lastName = userData.last_name
        state.ltiID = userData.lti_id
        state.gradeNotifications = userData.grade_notifications
        state.commentNotifications = userData.comment_notifications
        state.permissions = permissions
    },
    [types.LOGOUT] (state) {
        state.jwtAccess = null
        state.jwtRefresh = null
        state.uID = null
        state.username = null
        state.email = null
        state.verifiedEmail = null
        state.profilePicture = null
        state.firstName = null
        state.lastName = null
        state.ltiID = null
        state.gradeNotifications = null
        state.commentNotifications = null
        state.permissions = null
    },
    [types.SET_GRADE_NOTIFICATION] (state, val) {
        state.gradeNotifications = val
    },
    [types.SET_COMMENT_NOTIFICATION] (state, val) {
        state.commentNotifications = val
    },
    [types.EMAIL_VERIFIED] (state) {
        state.verifiedEmail = true
    },
    [types.SET_FULL_USER_NAME] (state, data) {
        state.firstName = data.firstName
        state.lastName = data.lastName
    },
    [types.SET_PROFILE_PICTURE] (state, dataURL) {
        state.profilePicture = dataURL
    },
    [types.UPDATE_PERMISSIONS] (state, data) {
        const permissions = data.permissions
        const permissionKey = data.key

        state.permissions[permissionKey] = permissions
    }

}

const actions = {
    login ({ commit, dispatch }, { username, password }) {
        return new Promise((resolve, reject) => {
            connection.conn.post('/token/', {username: username, password: password}).then(response => {
                commit(types.LOGIN, response.data)

                dispatch('populateStore').then(response => {
                    resolve('JWT and store are set succesfully.')
                }, error => {
                    Vue.toasted.error(error.response.description)
                    reject(error) // Login success but hydration failed
                })
            }, error => {
                reject(error) // Login failed, hydration failed.
            })
        })
    },
    logout ({commit, state}) {
        return Promise.all([
            // Example how to access different module mutation: commit(`module/${types.MUTATION_TYPE}`, null, { root: true })
            commit(types.LOGOUT)
        ])
    },
    verifyLogin ({ commit, dispatch, getters }, error = null) {
        console.log('Verifying login')
        return new Promise((resolve, reject) => {
            if (!getters.jwtRefresh || (error !== null && error.response.data.code !== 'token_not_valid')) {
                reject(error || Error('No valid token')) // We either dont have a refresh token or the server errored due to something other than the validity fo the token.
            } else {
                connection.conn.post('token/refresh/', {refresh: getters.jwtRefresh}).then(response => {
                    // Already logged in, update state
                    console.log('Check if the data contains access and refresh keys.')
                    console.log(response.data)
                    commit(types.LOGIN, response.data)

                    if (!getters.storePopulated) { // TODO Decide if its safer to simply always repopulate the store!
                        dispatch('populateStore')
                            .then(_ => { resolve() })
                            .catch(error => { reject(error) })
                    } else {
                        resolve('JWT refreshed succesfully, store was already populated.')
                    }
                }, error => {
                    commit(types.LOGOUT)
                    reject(error) // Token invalid
                })
            }
        })
    },
    populateStore ({ commit }) {
        return new Promise((resolve, reject) => {
            connection.conn.get('/get_user_store_data/').then(response => {
                commit(types.HYDRATE_USER, response.data)
                resolve('Store is populated succesfully')
            }, error => {
                console.log('Store populated unsuccessfully.')
                Vue.toasted.error(error.response.description)
                reject(error)
            })
        })
    }
}

export default {
    namespaced: true,
    state: {
        jwtAccess: null,
        jwtRefresh: null,
        uID: null,
        username: null,
        email: null,
        verifiedEmail: false,
        profilePicture: null,
        firstName: null,
        lastName: null,
        ltiID: null,
        gradeNotifications: null,
        commentNotifications: null,
        permissions: null
    },
    getters,
    mutations,
    actions
}
