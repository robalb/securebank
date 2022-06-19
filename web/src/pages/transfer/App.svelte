<script>
  import Layout from '../../components/Layout.svelte'
  let hexInput;
  let hexInputError = ""

  function handleSubmit(e){

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
        <input bind:this={hexInput} 
         type="text" required pattern="[a-f\d]*" maxLength="20" minLength="20"
         title="Lowercase hexadecimal value is required"
         class="form-95" placeholder="From account ID">

        <input 
         type="text" required pattern="[a-f\d]*" maxLength="20" minLength="20"
         title="Lowercase hexadecimal value is required"
         class="form-95" placeholder="To account ID">
       </div>
       <div class="row">
          <input 
           type="number" required pattern="[a-f\d]*" maxLength="20" minLength="20"
           title="Lowercase hexadecimal value is required"
           class="form-95" placeholder="amount">

          <button class="btn btn-primary">Transfer</button>
       </div>
      </form>

      {#if hexInputError}
        <div class="error">
          <img src={errorImg} aria-role="presentation" />
          <p>{hexInputError}</p>
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
