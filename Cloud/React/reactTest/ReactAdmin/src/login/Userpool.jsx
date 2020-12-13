import { CognitoUserPool } from 'amazon-cognito-identity-js';

const poolData = {
    UserPoolId: 'us-east-1_dIorW7bdh',
    ClientId: '298qj65q9coa3k42uov726a2dn',
  };

export default new CognitoUserPool(poolData);

  