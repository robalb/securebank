
//This is a VITE env variable
// https://vitejs.dev/guide/env-and-mode.html
const IS_PRODUCTION = import.meta.env.PROD

/**
 * Api endpoint url
 */
export const baseApiUrl = IS_PRODUCTION ?
  '/api/' :
  'http://localhost:8080/api/'
