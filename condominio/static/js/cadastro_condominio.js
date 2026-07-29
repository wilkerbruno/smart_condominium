class CEP {
  constructor(promise) {
    this._promise = promise;
  }

  then(resolve, reject) {
    return this._promise.then(resolve, reject);
  }

  catch(reject) {
    return this._promise.catch(reject);
  }

  static search(cep) {
    return new CEP(
      fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => {
          if (!response.ok) {
            throw new Error(response.status + ': ' + response.statusText);
          }

          return response.json();
        })
        .then(json => {
          const { logradouro, localidade, uf } = json;
          return { logradouro, localidade, uf };
        })
        .catch(error => {
          throw new Error(error[0] + ': ' + error[1]);
        })
    );
  }
}

String.prototype.isBrazilianZipCode = function() {
  return /^[0-9]{5}-?[0-9]{3}$/.test(this);
};

const getAddress = () => {
  const zipCode = document.getElementById('zip');
  const address = document.getElementById('address');
  const city = document.getElementById('city');
  const state = document.getElementById('state');
  
  if (zipCode.isBrazilianZipCode()) {
    CEP.search(zipCode.value)
      .then(data => {
        address.value = data.logradouro;
        city.value = data.localidade;
        state.value = data.uf;
      });
  }
};