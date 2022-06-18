<script>
  import Layout from '../components/Layout.svelte'
  import errorImg from '../assets/msg_error-0.png'
  import {baseApiUrl} from '../utils/api.js'
  import {showCurrency, showDate} from '../utils/conversions.js'

  //hex account id form input
  let hexInput;
  let hexInputError = ""

  //data fetched from the apis
  let data = {}

  async function fetchData(id){
    //fetch new data
    try{
      let res = await fetch(baseApiUrl + 'account/' + id)
      let resJson = await res.json()
      // Handle json errors
      if(!res.ok){
        if(resJson.detail == "invalid_id"){
          hexInputError =  'This account ID is not registered in the system';
        }
        else if(resJson.detail == "transaction_failed"){
          hexInputError =  'Internal transaction error. Your request failed';
        }
        else{
          hexInputError =  'Your request failed, in a way that no one could predict. Are you happy?';
        }
      }
      //data succesfully fetched, let svelte reactivity handle it
      else{
        //the specs require the latest trasaction to be bold.
        //Add extra attribute to latest tranaction,
        //And invert the array order for better visibility
        if(resJson.transactions && resJson.transactions.length > 0){
          resJson.transactions = resJson.transactions.reverse()
          resJson.transactions[0].first = true
        }
        data = resJson
        console.log(data)
      }
    }
    catch(e){
      hexInputError = 'Something went wrong. The APIs are unreachable';
      console.error(e)
    }
  }

  function handleSubmit(e){
    //bypass native element input validation
    if(!hexInput.validity.valid){
      e.preventDefault()
      showError()
      return
    }
    //remove previous input errors
    hexInputError= ''
    //remove previous data
    data = {}
    //fetch and display new data
    fetchData(hexInput.value)
  }

  function showError(){
    if(hexInput.validity.valid){
      hexInputError= ''
    } else if(hexInput.validity.valueMissing) {
      hexInputError= 'You need to enter an account ID';
    } else if(hexInput.validity.patternMismatch) {
      hexInputError= 'Only a-f lowercase letters and 0-9 nubers allowed';
    } else if(hexInput.validity.tooShort) {
      hexInputError= `Account ID should be at least ${ hexInput.minLength } characters; you entered ${ hexInput.value.length }.`;
    }
  }
</script>

<Layout currentPage={"/"}>
  <div class="container">

    <div class="card">
      <div class="card-header">
        <h4 class="my-0">Account Search</h4>
      </div>
      <div class="card-body">

      <form novalidate on:submit|preventDefault={handleSubmit}>
        <input bind:this={hexInput} 
         type="text" required pattern="[a-f\d]*" maxLength="20" minLength="20"
         title="Lowercase hexadecimal value is required"
         class="form-95" placeholder="enter an account id">
        <button class="btn btn-primary">Search</button>
      </form>

      {#if hexInputError}
        <div class="error">
          <img src={errorImg} aria-role="presentation" />
          <p>{hexInputError}</p>
        </div>
      {/if}

      <h5>User</h5>

      <table class="table ">
        <thead>
          {#if data.name}
            <tr>
              <th scope="col">Name: {data.name}</th>
              <th scope="col">Surname: {data.surname}</th>
              <th scope="col">Balance: {showCurrency(data.balance)}</th>
            </tr>
          {:else}
            <th scope="col">--</th>
          {/if}
        </thead>
      </table>

      <h5>Transactions</h5>

      <table class="table table-responsive-md table-hover">
        <thead>
          <tr>
            <th style="width: 100px;" scope="col">ID</th>
            <th scope="col">Sender</th>
            <th scope="col">Receiver</th>
            <th style="width: 100px;"scope="col">Amount</th>
            <th  scope="col">Time</th>
          </tr>
        </thead>
        {#if data.transactions}
        <tbody>
          {#each data.transactions as t }
            <tr class="{t.first && 'bold'}">
              <td>{t.id}</td>
              <td>{t.sender_id}</td>
              <td>{t.receiver_id}</td>
              <td>{showCurrency(t.amount)}</td>
              <td>{showDate(t.time)}</td>
            </tr>
          {/each}
        </tbody>
        {/if}
      </table>

    </div>
  </div>

</div>
</Layout>


<style>
  .container {
    margin: 2rem auto;
    padding: .5rem;
    max-width: 1000px;
    box-sizing: border-box;
    width: 100%;
  }
  form{
    display: flex;
    margin: 1rem 0;
    margin-top: .5rem;
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
  .table{
    background-color: #c0c0c0;
    border-top: 2px solid lightgrey;
    border-left: 2px solid lightgrey;
    border-right: 2px solid darkgrey;
    table-layout: fixed;
    width: 100%;
  }
  .table td{
    border-top: 2px solid lightgrey;
    border-bottom: 2px solid darkgrey;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
  }
  .table tr.bold{
    font-weight: bold;
  }
</style>
