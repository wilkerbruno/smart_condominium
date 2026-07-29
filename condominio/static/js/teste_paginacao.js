  document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 8; // Máximo de 8 linhas por página
    const tableBody = document.getElementById("myTableBody");
    const input = document.getElementById("search");

  // Dados fictícios para a tabela
  const data = [
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 311", cpf: "111111111", morador: "Luiz Miranda", telefone: "1212-1212", celular: "90111-1111", email: "luiz@example.com", status: "Normal" },
    { unidade: "U - 312", cpf: "121212121", morador: "Mariana Pinto", telefone: "1313-1313", celular: "90222-2222", email: "mariana@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    { unidade: "U - 301", cpf: "111111111", morador: "João Silva", telefone: "1111-1111", celular: "99999-9999", email: "joao@example.com", status: "Normal" },
    { unidade: "U - 302", cpf: "222222222", morador: "Maria Souza", telefone: "2222-2222", celular: "98888-8888", email: "maria@example.com", status: "Normal" },
    { unidade: "U - 303", cpf: "333333333", morador: "Carlos Lima", telefone: "3333-3333", celular: "97777-7777", email: "carlos@example.com", status: "Normal" },
    { unidade: "U - 304", cpf: "444444444", morador: "Ana Costa", telefone: "4444-4444", celular: "96666-6666", email: "ana@example.com", status: "Normal" },
    { unidade: "U - 305", cpf: "555555555", morador: "Pedro Santos", telefone: "5555-5555", celular: "95555-5555", email: "pedro@example.com", status: "Normal" },
    { unidade: "U - 306", cpf: "666666666", morador: "Lucas Oliveira", telefone: "6666-6666", celular: "94444-4444", email: "lucas@example.com", status: "Normal" },
    { unidade: "U - 307", cpf: "777777777", morador: "Fernanda Almeida", telefone: "7777-7777", celular: "93333-3333", email: "fernanda@example.com", status: "Normal" },
    { unidade: "U - 308", cpf: "888888888", morador: "Ricardo Ferreira", telefone: "8888-8888", celular: "92222-2222", email: "ricardo@example.com", status: "Normal" },
    { unidade: "U - 309", cpf: "999999999", morador: "Juliana Ribeiro", telefone: "9999-9999", celular: "91111-1111", email: "juliana@example.com", status: "Normal" },
    { unidade: "U - 310", cpf: "101010101", morador: "Paulo Araujo", telefone: "1010-1010", celular: "90000-0000", email: "paulo@example.com", status: "Normal" },
    
  
  ];
  const totalPages = Math.ceil(data.length / rowsPerPage);
  let currentPage = 1;

  const pageNumbers = document.getElementById("page-numbers");

  function displayRowsForPage(page) {
    tableBody.innerHTML = "";
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const rowsToDisplay = data.slice(start, end);

    rowsToDisplay.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.unidade}</td>
        <td>${row.cpf}</td>
        <td>${row.morador}</td>
        <td>${row.telefone}</td>
        <td>${row.celular}</td>
        <td>${row.email}</td>
        <td>${row.status}</td>
      `;
      tableBody.appendChild(tr);
    });
    highlightCurrentPage();
  }

  function createPageButtons() {
    pageNumbers.innerHTML = "";

    if (totalPages <= 5) {
      for (let i = 1; i <= totalPages; i++) {
        createPageButton(i);
      }
    } else {
      // Mostrar os 5 primeiros e o último
      for (let i = 1; i <= 5; i++) {
        createPageButton(i);
      }
      if (currentPage > 5 && currentPage < totalPages - 1) {
        const ellipsis = document.createElement("span");
        ellipsis.textContent = "...";
        ellipsis.className = "ellipsis";
        pageNumbers.appendChild(ellipsis);
        createPageButton(currentPage);
      }
      const ellipsis = document.createElement("span");
      ellipsis.textContent = "...";
      ellipsis.className = "ellipsis";
      pageNumbers.appendChild(ellipsis);
      createPageButton(totalPages);
    }
  }

  function createPageButton(page) {
    const button = document.createElement("button");
    button.textContent = page;
    button.className = "page-button";
    button.addEventListener("click", () => {
      currentPage = page;
      displayRowsForPage(currentPage);
      createPageButtons();
    });
    pageNumbers.appendChild(button);
  }

  function highlightCurrentPage() {
    const buttons = document.querySelectorAll(".page-button");
    buttons.forEach((button) => {
      if (parseInt(button.textContent) === currentPage) {
        button.classList.add("active");
      } else {
        button.classList.remove("active");
      }
    });
  }

  document.getElementById("prev").addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      displayRowsForPage(currentPage);
      createPageButtons();
    }
  });

  document.getElementById("next").addEventListener("click", () => {
    if (currentPage < totalPages) {
      currentPage++;
      displayRowsForPage(currentPage);
      createPageButtons();
    }
  });

  // Filtragem da tabela conforme o texto do input
  function searchFunction() {
    const filter = input.value.toUpperCase();
    const filteredData = data.filter(item => {
      return (
        item.unidade.toUpperCase().includes(filter) ||
        item.cpf.toUpperCase().includes(filter) ||
        item.morador.toUpperCase().includes(filter) ||
        item.telefone.toUpperCase().includes(filter) ||
        item.celular.toUpperCase().includes(filter) ||
        item.email.toUpperCase().includes(filter) ||
        item.status.toUpperCase().includes(filter)
      );
    });
    currentPage = 1; // Reinicia para a primeira página nos resultados filtrados
    updateTable(filteredData);
  }

  // Atualiza a tabela com os dados filtrados
  function updateTable(filteredData) {
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const rowsToDisplay = filteredData.slice(start, end);

    tableBody.innerHTML = "";

    rowsToDisplay.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.unidade}</td>
        <td>${row.cpf}</td>
        <td>${row.morador}</td>
        <td>${row.telefone}</td>
        <td>${row.celular}</td>
        <td>${row.email}</td>
        <td>${row.status}</td>
      `;
      tableBody.appendChild(tr);
    });

    // Atualiza paginação para os dados filtrados
    const totalPagesFiltered = Math.ceil(filteredData.length / rowsPerPage);
    if (totalPagesFiltered !== totalPages) {
      totalPages = totalPagesFiltered;
      createPageButtons();
    }
    highlightCurrentPage();
  }

  createPageButtons();
  displayRowsForPage(currentPage);

  // Adiciona o event listener para o campo de busca
  input.addEventListener("keyup", searchFunction);
});