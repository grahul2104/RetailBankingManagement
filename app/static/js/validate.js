(function($) {
  $.fn.inputFilter = function(inputFilter) {
    return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      } else {
        this.value = "";
      }
    });
  };
}(jQuery));


$(function(){
    $("input[name='name']").inputFilter(function(value) {return /^[a-z ]*$/i.test(value); });
	$("input[name='city']").inputFilter(function(value) {return /^[a-z]*$/i.test(value); });
	$("input[name='ssn_id']").inputFilter(function(value) {return /^\d*$/.test(value); });
	$("input[name='cust_id']").inputFilter(function(value) {return /^\d*$/.test(value); });
	$("input[name='acc_id']").inputFilter(function(value) {return /^\d*$/.test(value); });
	$("input[name='source_acc_id']").inputFilter(function(value) {return /^\d*$/.test(value); });
	$("input[name='target_acc_id']").inputFilter(function(value) {return /^\d*$/.test(value); });
	$("input[name='amount']").inputFilter(function(value) {return /^\d*$/.test(value); });
	$("input[name='age']").inputFilter(function(value) {return /^\d*$/.test(value); });
	$("input[name='no_of_transactions']").inputFilter(function(value) {return /^\d*$/.test(value); });
});


$(function(){
      $("form").validate({
    rules: {
      name: "required",
      username: "required",
      state: "required",
      city: "required",
      address: "required",
      age: {
        required: true,
        maxlength: 3,
        },
      ssn_id: {
        required: true,
        minlength: 9,
        maxlength: 9,
        },
      cust_id: {
        required: true,
        minlength: 9,
        maxlength: 9,
        },
      acc_id: {
        required: true,
        minlength: 9,
        maxlength: 9,
        },
      password: {
        required: true,
        minlength: 8
      },
    },
    messages: {
      name: {
        required: "Please enter the Full Name",
      },
      username: {
        required: "Please enter your Username",
      },
      password: {
        required: "Please provide your password",
        minlength: "Your password must be at least 8 characters long"
      },
      age: {
        required: "Please provide an age",
        maxlength: "Age should be greater than 3 digits",
      },
      ssn_id: {
        required: "Please provide a SSN ID",
        minlength: "SSN ID should be 9 digits long",
        maxlength: "SSN ID should be 9 digits long",
      },
      acc_id: {
        required: "Please provide the Account ID",
        minlength: "Account ID should be 9 digits long",
        maxlength: "Account ID should be 9 digits long",
      },
      cust_id: {
        required: "Please provide the Customer ID ",
        minlength: "Customer ID should be 9 digits long",
        maxlength: "Customer ID should be 9 digits long",
      },
      source_acc_id: {
        required: "Please provide the Source Account ID",
        minlength: "Account ID should be 9 digits long",
        maxlength: "Account ID should be 9 digits long",
      },
      target_acc_id: {
        required: "Please provide the Target Account ID",
        minlength: "Account ID should be 9 digits long",
        maxlength: "Account ID should be 9 digits long",
      },
      state: "Please select your state",
      city: "Please provide your city",
      address: "Please provide your address",
    },
    submitHandler: function(form) {
      $('input[type=radio]').prop('disabled', true);
      form.submit();
    }
  });
});