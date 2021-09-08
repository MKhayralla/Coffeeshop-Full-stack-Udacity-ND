/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-vy99-vnq.us', // the auth0 domain prefix
    audience: 'https://drinks.udacity.api', // the audience set for the auth0 app
    clientId: 'ms4UMzsXud6Dc6Qc1ihmRhNSwbOsY9Q5', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:3000', // the base url of the running ionic application. 
  }
};
