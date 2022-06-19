<script>
  import Layout from '../../components/Layout.svelte'
  import errorImg from '../../assets/msg_error-0.png'
  import successImg from '../../assets/check-0.png'
  import shareImg from '../../assets/transfer.png'
  let fromInput;
  let toInput;
  let amountInput;
  let displayError = ""
  let states = {
    idle: "IDLE",
    loading: "LOADING",
    success: "SUCCESS",
    fail: "FAIL"
  }
  let state = states.idle

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
         type="text" required pattern="[a-f\d]*" maxLength="20" minLength="20"
         title="Lowercase hexadecimal value is required"
         class="form-95" placeholder="From account ID">

        <img src={shareImg} aria-role="presentation" width="80" style="height:auto; margin: 0 1rem;" />

        <input bind:this={toInput} 
         type="text" required pattern="[a-f\d]*" maxLength="20" minLength="20"
         title="Lowercase hexadecimal value is required"
         class="form-95" placeholder="To account ID">
       </div>
       <div class="row">
          <input bind:this={amountInput}
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

      {#if state == states.idle || state == states.loading}
      <div class="progress">
        <div class="progress-bar "
          role="progressbar" style="width: 0%"
          aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"
          >
        </div>
      </div>
      {/if}

      {#if state == states.success}
        <div class="error">
          <img src={successImg} aria-role="presentation" />
          <p>{displayError}</p>
        </div>
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
