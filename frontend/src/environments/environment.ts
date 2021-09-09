

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'your auth0 tenant', // the auth0 domain prefix
    audience: 'your API identifier', // the audience set for the auth0 app
    clientId: 'your application clientID', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:3000', // the base url of the running ionic application. 
  }
};
