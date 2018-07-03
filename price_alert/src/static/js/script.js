function viewPassword(input, status)
{
  var passwordInput = input;
  var passStatus = status;

  if (passwordInput.type == 'password'){
    passwordInput.type='text';
    passStatus.className='fa fa-eye-slash';

  }
  else{
    passwordInput.type='password';
    passStatus.className='fa fa-eye';
  }
};

