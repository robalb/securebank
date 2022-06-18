  <script>
  import explorer from '../assets/msie1-2.png'
  import netscape from '../assets/netscape.png'
  </script>
  <footer>
  <p>This website requires a browser with JavaScript support</p>
  <img src={netscape} width=30 alt="msie logo" />
  <img src={explorer} width=30 alt="netscape logo" />
  </footer>

  <style>
  footer{
    display:flex;
    align-items:center;
    justify-content:center;
    margin: 0 auto;
    max-width: 390px;
  }
  p{
    padding: 1rem;
    margin: 0;
  }
  img{
    margin-right: 1rem;
  }
  </style>

