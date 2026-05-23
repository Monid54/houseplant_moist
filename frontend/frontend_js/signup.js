const phoneInput = document.querySelector("input[name='phone']");

if (phoneInput) {
  window.intlTelInput(phoneInput, {
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@18.1.1/build/js/utils.js",
    initialCountry: "auto",
    geoIpLookup: callback => {
      fetch('https://ipapi.co/json')
        .then(res => res.json())
        .then(data => callback(data.country_code))
        .catch(() => callback('US'));
    },
    nationalMode: false,
  });
}

fetch('https://restcountries.com/v3.1/all')
  .then(response => response.json())
  .then(data => {

    const select =
      document.querySelector('select[name="country"]');

    const sortedCountries = data
      .map(country => ({
        name: country.name.common,
        code: country.cca2
      }))
      .sort((a, b) =>
        a.name.localeCompare(b.name)
      );

    select.innerHTML =
      '<option value="">Select Country</option>';

    sortedCountries.forEach(country => {

      const option =
        document.createElement('option');

      option.value = country.code;
      option.textContent = country.name;

      select.appendChild(option);
    });

  })
  .catch(error => {
    console.error(
      'Failed to load countries:',
      error
    );
  });

document
  .getElementById("signupForm")
  .addEventListener("submit", function(e) {

    e.preventDefault();

    const firstname =
      document.querySelector(
        'input[name="firstname"]'
      ).value;

    const lastname =
      document.querySelector(
        'input[name="lastname"]'
      ).value;

    const country =
      document.querySelector(
        'select[name="country"]'
      ).value;

    const phone =
      document.querySelector(
        'input[name="phone"]'
      ).value;

    localStorage.setItem(
      "signupData",
      JSON.stringify({
        firstname,
        lastname,
        country,
        phone
      })
    );

    window.location.href =
      "create_account.html";
});