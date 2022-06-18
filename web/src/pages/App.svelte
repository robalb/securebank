<script>
  import Layout from '../components/Layout.svelte'
  import errorImg from '../assets/msg_error-0.png'

  let hexInput;

  let hexInputError = ""

  function handleSubmit(e){
    //bypass native element input validation
    if(!hexInput.validity.valid){
      e.preventDefault()
      showError()
      return
    }

    const formData = new FormData(e.target);
    hexInput.setCustomValidity("id not found in the system")
    hexInput.reportValidity()
    console.log(formData)
    console.log(e)
    console.log(hexInput)

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
         class="form-95" placeholder="enter a user id">
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
          <tr>
            <th scope="col">First</th>
            <th scope="col">Last</th>
            <th scope="col">Handle</th>
          </tr>
        </thead>
      </table>

<h5>Transactions</h5>

<table class="table ">
  <thead>
    <tr>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
    </tr>
    <tr>
      <td>Larry</td>
      <td>the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table>

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
    background-color: #dfdfdf;
    padding: .25;
    display: flex;
    align-items: center;
  }
  .table{
    background-color: #c0c0c0;
    border-top: 2px solid white;
    border-left: 2px solid white;
    border-right: 2px solid darkgrey;
  }
  .table td{
    border-top: 2px solid white;
    border-bottom: 2px solid darkgrey;
  }
</style>
