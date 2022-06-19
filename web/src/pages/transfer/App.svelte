<script>
  import Layout from '../../components/Layout.svelte'
  import errorImg from '../../assets/msg_error-0.png'
  import successImg from '../../assets/check-0.png'
  import shareImg from '../../assets/transfer.png'
  import {baseApiUrl} from '../../utils/api.js'
  import {showCurrency, showDate, toCents} from '../../utils/conversions.js'

  //form elements refs
  let fromInput;
  let toInput;
  let amountInput;
  let displayError = ""

  //data fetched from the apis
  let data = {}

  async function APICall(body, form){
    try{
      let res = await fetch(baseApiUrl + 'transfer/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })
      let resJson = await res.json()
      // Handle json errors
      if(!res.ok){
        if(resJson.detail == "invalid_id"){
          displayError =  'One of the account IDs you entered is not registered in the system';
        }
        else if(resJson.detail == "transaction_failed"){
          displayError =  'Internal transaction error. Your request failed';
        }
        else if(resJson.detail == "insufficient_credit"){
          displayError =  'Insufficient credit to complete the transaction';
        }
        else{
          displayError =  'Your request failed, in a way that no one could predict.';
        }
      }
      //data succesfully fetched, let svelte reactivity handle it
      else{
        form.reset()
        data = resJson
        console.log(data)
      }
    }
    catch(e){
      displayError = 'Something went wrong. The APIs are unreachable';
      console.error(e)
    }

  }

  function handleSubmit(e){
    //bypass native element input validation
    let inputs = [
      fromInput,
      toInput,
      amountInput
    ]
    for (let input of inputs){
      if(!input.validity.valid){
        e.preventDefault()
        showError(input)
        return
      }
    }
    //remove previous input errors
    displayError= ''
    //remove previous data
    data = {}
    //get form input data in json format, using modern DOM apis
    const dataRaw = new FormData(e.target);
    const dataJson = Object.fromEntries(dataRaw.entries());
    //convert amount, since the APIs expect amount values expressed in cents
    dataJson.amount = toCents(dataJson.amount)
    //perform api call
    APICall(dataJson, e.target)
  }

  function showError(input){
    let isText = input.type.toUpperCase() == "TEXT"
    //no errors
    if(input.validity.valid){
      displayError= ''
    } 
    //text errors
    else if(isText && input.validity.valueMissing) {
      displayError= 'You need to enter an account ID';
    } else if(isText && input.validity.patternMismatch) {
      displayError= 'Only a-f lowercase letters and 0-9 nubers allowed';
    } else if(isText && input.validity.tooShort) {
      displayError= `Account ID should be at least ${ input.minLength } characters; you entered ${ input.value.length }.`;
    }
    //numeric errors
    else if(input.validity.valueMissing) {
      displayError= 'You need to enter a transfer amount';
    } else if(input.validity.rangeUnderflow) {
      displayError= 'Transfer Amount should be positive. You entered '+ input.value
    } else if(input.validity.stepMismatch) {
      displayError= 'Transfer Amount '+ input.value + ' has too many decimal places. Only 2 allowed'
    } else if(input.validity.badInput) {
      displayError= 'The value you entered is not a valid transfer amount.'
    }
  }
</script>

<Layout currentPage={"/transfer/"}>
  <div class="container">

    <div class="card">
      <div class="card-header">
        <h4 class="my-0">Transfer</h4>
      </div>
      <div class="card-body">

      <form novalidate on:submit|preventDefault={handleSubmit}>
      <div class="row">
        <input bind:this={fromInput} 
         name="from"
         type="text" required pattern="[a-f\d]*" maxLength="20" minLength="20"
         title="Lowercase hexadecimal value is required"
         class="form-95" placeholder="From account ID">

        <img src={shareImg} aria-role="presentation" width="80" style="height:auto; margin: 0 1rem;" />

        <input bind:this={toInput} 
         name="to"
         type="text" required pattern="[a-f\d]*" maxLength="20" minLength="20"
         title="Lowercase hexadecimal value is required"
         class="form-95" placeholder="To account ID">
       </div>
       <div class="row">
          <input bind:this={amountInput}
           name="amount"
           type="number" required min="0" step=".01"
           title="a numeric value is required"
           class="form-95" placeholder="amount &euro;">

          <button class="btn btn-primary">Transfer</button>
       </div>
      </form>

      {#if displayError}
        <div class="error">
          <img src={errorImg} aria-role="presentation" />
          <p>{displayError}</p>
        </div>
      {/if}

      {#if data.transaction}
        <div class="error">
          <img src={successImg} aria-role="presentation" />
          <p>Transfer successful</p>
        </div>
        <p>transaction id: {data.transaction}</p>
        <p>sender now has a balance of: {showCurrency(data.balance_from)}</p>
        <p>receiver now has a balance of: {showCurrency(data.balance_to)}</p>
      {/if}

      </div>
    </div>
  </div>
</Layout>

<style>
  .container {
    margin: 2rem auto;
    padding: .5rem;
    max-width: 800px;
    box-sizing: border-box;
    width: 100%;
  }
  form{
    margin: 1rem 0;
    margin-top: .5rem;
    box-sizing: border-box;
  }
  .row{
    box-sizing: border-box;
    flex-wrap: nowrap;
    margin: 0;
    margin-bottom: 1rem;
    align-items:center;
  }
  form button{
    margin-left: 1rem;
  }
  .error{
    padding: .5;
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }
  .error p{
    margin: 0 0 0 1rem;
  }

</style>
