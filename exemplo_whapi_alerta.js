const https = require('https');

// Token de acesso da API do Whapi.Cloud (Sandbox)
const WHAPI_TOKEN = 'YuOAsd5Lgg3bOMZOgueq5KRMB8Zhzlwu';

// Nível crítico (X) para disparar o alerta
const NIVEL_CRITICO = 5.0;

// Lista de contatos autorizados no Sandbox
// Formato: DDI + DDD + Número (ex: 5511999999999)
const CONTATOS = [
  '',
  '5519992544874',
  '5519997490041',
  ''
];

/**
 * Função para enviar mensagem de WhatsApp via Whapi.Cloud
 * @param {string} to Número de telefone do destinatário
 * @param {string} message Texto da mensagem
 */
function enviarMensagemWhatsApp(to, message) {
  const data = JSON.stringify({
    to: `${to}@s.whatsapp.net`,
    body: message
  });

  const options = {
    hostname: 'gate.whapi.cloud',
    path: '/messages/text',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${WHAPI_TOKEN}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  };

  const req = https.request(options, (res) => {
    let responseBody = '';

    res.on('data', (chunk) => {
      responseBody += chunk;
    });

    res.on('end', () => {
      if (res.statusCode === 200) {
        console.log(`✅ Alerta enviado para ${to} com sucesso.`);
      } else {
        console.error(`❌ Falha ao enviar para ${to}. Status: ${res.statusCode} | Erro: ${responseBody}`);
      }
    });
  });

  req.on('error', (error) => {
    console.error(`Erro na requisição para ${to}: ${error.message}`);
  });

  req.write(data);
  req.end();
}

/**
 * Função que verifica o nível da enchente e dispara mensagens se atingir o nível X
 * @param {string} nomeRio Nome do rio sendo monitorado
 * @param {number} nivelEnchente Nível atual da água
 */
function verificarEnchente(nomeRio, nivelEnchente) {
  console.log(`\nVerificando nível do ${nomeRio}: ${nivelEnchente}m (Nível crítico: ${NIVEL_CRITICO}m)`);

  if (nivelEnchente >= NIVEL_CRITICO) {
    console.log(`⚠️ Nível crítico atingido no ${nomeRio}! Disparando alertas...`);

    const mensagemAlerta = `⚠️ ALERTA: O nível do *${nomeRio}* atingiu ${nivelEnchente}m, nível crítico! Evite áreas de risco nas proximidades.`;

    CONTATOS.forEach(numero => {
      enviarMensagemWhatsApp(numero, mensagemAlerta);
    });
  } else {
    console.log('✅ Nível seguro. Nenhum alerta necessário.');
  }
}

// ==========================================
// Simulação de Testes
// ==========================================

// Simula nível seguro (não deve enviar mensagem)
setTimeout(() => {
  verificarEnchente('Rio Tietê', 3.2);
}, 1000);

// Simula nível crítico (deve disparar os 5 alertas)
setTimeout(() => {
  verificarEnchente('Rio Piracicaba', 5.5);
}, 3000);
