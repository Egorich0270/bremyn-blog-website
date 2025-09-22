function resizeCanvas(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const displayWidth = canvas.clientWidth * dpr;
    const displayHeight = canvas.clientHeight * dpr;

    if (canvas.width !== displayWidth || canvas.height !== displayHeight) {
        canvas.width = displayWidth;
        canvas.height = displayHeight;
    }

    const gl = canvas.getContext("webgl");
    gl.viewport(0, 0, canvas.width, canvas.height);
}

// Вызовите resizeCanvas один раз, а также после изменения размера окна

var vs = `
precision mediump float;

attribute vec2 verPosition;
uniform float u_time;

void main() {
    gl_Position = vec4(verPosition, 0.0, 1.0);
}
`;

var fs = `
precision mediump float;

uniform float u_time;  // Униформа для времени
uniform vec2 u_resolution;

void main() {
    vec2 st = gl_FragCoord.xy / u_resolution;
    // Пример использования времени: изменяем цвет в зависимости от времени
    gl_FragColor = vec4(st.x, st.x, st.x, 1.0);
}
`;

var canvas = document.getElementById("canvas");
var gl = canvas.getContext("webgl");
resizeCanvas(canvas);
window.addEventListener("resize", () => resizeCanvas(canvas));
gl.clearColor(0.2, 0.5, 0.7, 1);
gl.clear(gl.COLOR_BUFFER_BIT);

// Создание и компиляция вершинного шейдера
var vShader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vShader, vs);
gl.compileShader(vShader);
if (!gl.getShaderParameter(vShader, gl.COMPILE_STATUS)) {
    console.error("Ошибка компиляции вершинного шейдера:", gl.getShaderInfoLog(vShader));
}

// Функция для пересоздания программы с новым фрагментным шейдером
function createProgramWithNewFragmentShader(gl, vertexShader, fragmentShaderSource) {
    const newFragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(newFragmentShader, fragmentShaderSource);
    gl.compileShader(newFragmentShader);

    // Проверяем компиляцию фрагментного шейдера
    if (!gl.getShaderParameter(newFragmentShader, gl.COMPILE_STATUS)) {
        console.error("Ошибка компиляции фрагментного шейдера:", gl.getShaderInfoLog(newFragmentShader));
        gl.deleteShader(newFragmentShader);
        return null;
    }

    // Создаем новую программу и связываем шейдеры
    const newProgram = gl.createProgram();
    gl.attachShader(newProgram, vertexShader);
    gl.attachShader(newProgram, newFragmentShader);
    gl.linkProgram(newProgram);

    // Проверяем линковку программы
    if (!gl.getProgramParameter(newProgram, gl.LINK_STATUS)) {
        console.error("Ошибка линковки программы:", gl.getProgramInfoLog(newProgram));
        gl.deleteProgram(newProgram);
        return null;
    }

    // Удаляем шейдер после того, как он стал частью программы
    gl.deleteShader(newFragmentShader);

    return newProgram;
}

// Инициализация программы
var program = createProgramWithNewFragmentShader(gl, vShader, fs);
gl.useProgram(program);

// Определение вершин
var vArr = new Float32Array([
    1.0, 1.0,
    -1.0, -1.0,
    1.0, -1.0,

    1.0, 1.0,
    -1.0, -1.0,
    -1.0, 1.0,
]);
var vBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
gl.bufferData(gl.ARRAY_BUFFER, vArr, gl.STATIC_DRAW);

// Атрибут позиции
var position = gl.getAttribLocation(program, "verPosition");
gl.vertexAttribPointer(position, 2, gl.FLOAT, false, Float32Array.BYTES_PER_ELEMENT * 2, 0);
gl.enableVertexAttribArray(position);

// Униформы
var uTimeLocation = gl.getUniformLocation(program, "u_time");
var uResolutionLocation = gl.getUniformLocation(program, "u_resolution");

var textar = document.getElementById('myTextarea');

function render(time) {
    // Обновляем фрагментный шейдер, если текст в textarea изменился
    const newProgram = createProgramWithNewFragmentShader(gl, vShader, textar.value);
    if (newProgram) {
        gl.useProgram(newProgram);
        program = newProgram;

        // Обновляем локации униформ
        uTimeLocation = gl.getUniformLocation(program, "u_time");
        uResolutionLocation = gl.getUniformLocation(program, "u_resolution");

        // Устанавливаем атрибут позиции
        position = gl.getAttribLocation(program, "verPosition");
        gl.vertexAttribPointer(position, 2, gl.FLOAT, false, Float32Array.BYTES_PER_ELEMENT * 2, 0);
        gl.enableVertexAttribArray(position);
    }

    // Очищаем буфер
    gl.clear(gl.COLOR_BUFFER_BIT);

    // Передаем значения униформ
    gl.uniform2f(uResolutionLocation, canvas.width, canvas.height);
    gl.uniform1f(uTimeLocation, time * 0.001);

    // Рисуем
    gl.drawArrays(gl.TRIANGLES, 0, 6);

    requestAnimationFrame(render);
}

// Запускаем отрисовку
requestAnimationFrame(render);
