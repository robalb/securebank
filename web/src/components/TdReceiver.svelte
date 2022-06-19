<script>
  import depositImg from '../assets/transfer_to.png'
  import withdrawalImg from '../assets/transfer_from.png'
  export let amount;
  export let uid;
</script>

  {#if uid}
    {uid}
  {:else if amount > 0}
    <img src={depositImg} width="35" alt="deposit icon" role="presentation" />
    Deposit
  {:else}
    <img src={withdrawalImg} width="35" alt="withdrawal icon" role="presentation" />
    Withdrawal
  {/if}
