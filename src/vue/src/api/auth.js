import connection from '@/api/connection'
import statuses from '@/utils/constants/status_codes.js'
import router from '@/router'
import store from '@/store'

const errorsToRedirect = new Set([
    statuses.FORBIDDEN,
    statuses.NOT_FOUND,
    statuses.INTERNAL_SERVER_ERROR
])

/*
 * Redirects the following unsuccessfull request responses:
 * UNAUTHORIZED to Login, logs the client out and clears store.
 * FORBIDDEN, NOT_FOUND, INTERNAL_SERVER_ERROR to Error page.
 *
 * The response is thrown and further promise handling should take place.
 * This because this is generic response handling, and we dont know what should happen in case of an error.
 */
function handleError (error, noRedirect = false) {
    const response = error.response
    const status = response.status

    if (status === statuses.UNAUTHORIZED) {
        store.commit('user/LOGOUT')
        router.push({name: 'Login'})
    } else if (!noRedirect && errorsToRedirect.has(status)) {
        router.push({name: 'ErrorPage',
            params: {
                code: status,
                reasonPhrase: response.statusText,
                description: response.data.description
            }
        })
    }

    throw error
}

function validatedSend (func, url, data = null, noRedirect = false) {
    store.loadingApiRequests++
    return func(url, data).then(
        resp => {
            store.loadingApiRequests--
            return resp
        }, error =>
            store.dispatch('user/validateToken', error).then(_ =>
                func(url, data).then(resp => {
                    store.loadingApiRequests--
                    return resp
                })
            )
    ).catch(error => {
        store.loadingApiRequests--
        return handleError(error, noRedirect)
    })
}

function improveUrl (url, data = null) {
    if (url[0] !== '/') url = '/' + url
    if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
    if (data) {
        url += '?'
        for (var key in data) { url += key + '=' + encodeURIComponent(data[key]) + '&' }
        url = url.slice(0, -1)
    }

    return url
}
/*
 * Previous functions are 'private', following are 'public'.
 */
export default {

    /* Create a user and add it to the database. */
    register (username, password, firstname, lastname, email, jwtParams = null) {
        return connection.conn.post('/users/', {
            username: username,
            password: password,
            first_name: firstname,
            last_name: lastname,
            email: email,
            jwt_params: jwtParams
        })
            .then(response => { return response.data.user })
    },

    /* Change password. */
    changePassword (newPassword, oldPassword) {
        return this.update('users/password', { new_password: newPassword, old_password: oldPassword })
    },

    /* Forgot password.
     * Checks if a user is known by the given email or username. Sends an email with a link to reset the password. */
    forgotPassword (username, email) {
        return connection.conn.post('/forgot_password/', {username: username, email: email})
    },

    /* Recover password */
    recoverPassword (username, recoveryToken, newPassword) {
        return connection.conn.post('/recover_password/', {username: username, recovery_token: recoveryToken, new_password: newPassword})
    },

    get (url, data = null, noRedirect = false) {
        url = improveUrl(url, data)
        return validatedSend(connection.conn.get, url, null, noRedirect)
    },
    post (url, data, noRedirect = false) {
        url = improveUrl(url)
        return validatedSend(connection.conn.post, url, data, noRedirect)
    },
    patch (url, data, noRedirect = false) {
        url = improveUrl(url)
        return validatedSend(connection.conn.patch, url, data, noRedirect)
    },
    delete (url, data = null, noRedirect = false) {
        url = improveUrl(url, data)
        return validatedSend(connection.conn.delete, url, null, noRedirect)
    },
    uploadFile (url, data, noRedirect = false) {
        url = improveUrl(url)
        return validatedSend(connection.connFile.post, url, data, noRedirect)
    },
    uploadFileEmail (url, data, noRedirect = false) {
        url = improveUrl(url)
        return validatedSend(connection.connFileEmail.post, url, data, noRedirect)
    },
    downloadFile (url, data, noRedirect = false) {
        url = improveUrl(url, data)
        return validatedSend(connection.connFile.get, url, null, noRedirect)
    },

    create (url, data, noRedirect = false) { return this.post(url, data, noRedirect) },
    update (url, data, noRedirect = false) { return this.patch(url, data, noRedirect) }
}
