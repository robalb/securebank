/**
* The webapp global locale
*/
export const locale = 'en-GB'

/**
* convert centesimal values received from the apis
* into a readable, localized format
* 
* @param value string - the integer value to convert
* @return string - the converted value
*/
export function showCurrency(value){
  value = value/100
  return (new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'EUR' }).format(value));
}

/**
* Convert UNIX Timestamps received from the apis into
* a readable, localized date
*/
export function showDate(timestamp){
  let date = new Date(timestamp * 1000)
  let settings = {
    dateStyle: 'short',
    timeStyle: 'short',
  }
  return (new Intl.DateTimeFormat('en-GB', settings).format(date));
}
