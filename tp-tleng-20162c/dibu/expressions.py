# coding=utf-8
from dibu.exceptions import SemanticException, SyntacticException


class Program(object):
    def __init__(self):
        self.lines = []

    def add(self, code_line):
        # CodeLineValidator().validate(code_line)
        self.lines.append(code_line)

    def evaluate(self):
        return self.header() + self.evaluate_code_lines() + self.footer()

    def header(self):
        height, width = self.size_in_code_lines()
        return '<?xml version="1.0" ?><svg baseProfile="full" height="' + height + '" version="1.1" width="' + width + '" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">'

    def footer(self):
        return '</svg>'

    def evaluate_code_lines(self):
        result = ""
        for code_line in self.lines:
            result += code_line.evaluate()
        return result

    def size_in_code_lines(self):
        size_lines = filter(lambda line: line.identifier == 'size', self.lines)
        if len(size_lines) > 1:
            raise SemanticException('No puede haber más de una línea "size"')
        elif len(size_lines) == 1:
            height = filter(lambda parameter: parameter.parameter_name == 'height', size_lines[0].parameters)[0].literal
            width = filter(lambda parameter: parameter.parameter_name == 'width', size_lines[0].parameters)[0].literal
            return str(height), str(width)
        else:
            return "200", "200"


class CodeLine(object):
    def __init__(self, identifier, parameters):
        self.identifier = identifier
        self.parameters = parameters

    def identifier_translations(self):
        return {'polygon': 'polygon',
                'rectangle': 'rect',
                'line': 'line',
                'circle': 'circle',
                'ellipse': 'ellipse',
                'polyline': 'polyline',
                'text': 'text'}

    def obligatory_parameters_for_identifier(self):
        return {'polygon': ['points'],
                'rectangle': ['upper_left', 'size'],
                'line': ['from', 'to'],
                'circle': ['center', 'radius'],
                'ellipse': ['center', 'rx', 'ry'],
                'polyline': ['points'],
                'text': ['t', 'at'],
                'size': ['height', 'width']}

    def valid_parameters(self):
        return {'polygon': ['points', 'fill', 'stroke', 'stroke-width', 'style'],
                'rectangle': ['upper_left', 'size', 'fill', 'stroke', 'stroke-width', 'style'],
                'line': ['from', 'to', 'fill', 'stroke', 'stroke-width', 'style'],
                'circle': ['center', 'radius', 'fill', 'stroke', 'stroke-width', 'style'],
                'ellipse': ['center', 'rx', 'ry', 'fill', 'stroke', 'stroke-width', 'style'],
                'polyline': ['points', 'fill', 'stroke', 'stroke-width', 'style'],
                'text': ['t', 'at', 'font-family', 'font-size', 'fill', 'stroke', 'stroke-width', 'style'],
                'size': ['height', 'width', 'fill', 'stroke', 'stroke-width', 'style']}

    def evaluate(self):
        self.validate_correct_code_line()

        if self.identifier == 'text':
            return "<" + self.identifier_translations()[
                self.identifier] + ' ' + self.evaluate_parameters_of_text() + ">" + self.evaluate_text() + '</text>'
        elif self.identifier == 'size':
            return ""
        else:
            return "<" + self.identifier_translations()[self.identifier] + ' ' + self.evaluate_parameters() + "/>"

    def evaluate_parameters(self):
        result = ""
        for parameter in self.parameters:
            result += parameter.evaluate() + ' '
        return result

    def evaluate_parameters_of_text(self):
        result = ""
        if 'at' in [parameter.parameter_name for parameter in self.parameters]:
            result += filter(lambda parameter: parameter.parameter_name == 'at', self.parameters)[0].evaluate() + ' '
        else:
            raise SemanticException('Text debe tener el parámetro "at"')

        optional_parameters_result = self._optional_parameters_for_text()

        return result + optional_parameters_result

    def _optional_parameters_for_text(self):
        optional_parameters_result = ''
        text_optional_parameters = filter(
            lambda parameter: parameter.parameter_name == 'font-size' or parameter.parameter_name == 'font-family',
            self.parameters)
        if len(text_optional_parameters) > 0:
            optional_parameters_result = 'style="'
            for optional_parameter in text_optional_parameters:
                optional_parameters_result += optional_parameter.evaluate() + ';'
            optional_parameters_result += '"'

        return optional_parameters_result

    def evaluate_text(self):
        for parameter in self.parameters:
            if parameter.parameter_name == 't':
                return str(parameter.literal)[1:-1]
        raise SemanticException('Text debe tener el parámetro "t"')

    def validate_correct_code_line(self):
        self._validate_obligatory_parameters_are_in_code_line()
        self._validate_only_valid_parameter_are_in_code_line()
        self._validate_not_duplicated_parameters()

    def _validate_obligatory_parameters_are_in_code_line(self):
        for parameter in self.obligatory_parameters_for_identifier()[self.identifier]:
            if parameter not in map(lambda parameter: parameter.parameter_name, self.parameters):
                raise SemanticException(
                    'El parámetro %s no está en la línea de código y es obligatorio.' % parameter)

    def _validate_not_duplicated_parameters(self):
        parameters_names = map(lambda parameter: parameter.parameter_name, self.parameters)
        for parameter_name in parameters_names:
            if len(filter(lambda param_name: param_name == parameter_name, parameters_names)) > 1:
                raise SemanticException('El parámetro %s está duplicado.' % parameter_name)

    def _validate_only_valid_parameter_are_in_code_line(self):
        for parameter in self.parameters:
            if parameter.parameter_name not in self.valid_parameters()[self.identifier]:
                raise SemanticException(
                    'El parámetro %s no es válido para el identificador %s' % (
                        parameter.parameter_name, self.identifier))


class Parameter(object):
    def __init__(self, parameter_name, literal):
        self.parameter_name = parameter_name
        self.literal = literal

    def parameter_function(self):
        return {'points': self.points_evaluate,
                'style': self.style_evaluate,
                'fill': self.fill_evaluate,
                'size': self.size_evaluate,
                'upper_left': self.upper_left_evaluate,
                'from': self.from_evaluate,
                'to': self.to_evaluate,
                'center': self.center_evaluate,
                'radius': self.radius_evaluate,
                'rx': self.rx_evaluate,
                'ry': self.ry_evaluate,
                'at': self.at_evaluate,
                'font-size': self.optional_text_parameter_evaluate,
                'font-family': self.optional_text_parameter_evaluate,
                'stroke': self.stroke_evaluate,
                'stroke-width': self.stroke_width_evaluate}

    def literal_type(self):
        return {
                'points': [list],
                'style': [str],
                'fill': [str],
                'size': [tuple],
                'upper_left': [tuple],
                'from': [tuple],
                'to': [tuple],
                'center': [tuple],
                'radius': [int, float],
                'rx': [int, float],
                'ry': [int, float],
                'at': [tuple],
                'font-size': [str],
                'font-family': [str],
                'stroke': [str],
                'stroke-width': [str]

        }

    def evaluate(self):
        self.validate_correct_parameter_types()
        return self.parameter_function()[self.parameter_name]()

    def validate_correct_parameter_types(self):
        if self.literal.__class__ not in self.literal_type()[self.parameter_name]:
            raise SyntacticException("Tipo incorrecto para parámetro %s" % self.parameter_name)

    def points_evaluate(self):
        result = 'points="'
        for point in self.literal:
            result += '%s,%s' % point + ' '
        result += '"'
        return result

    def style_evaluate(self):
        return 'style=' + self.literal

    def fill_evaluate(self):
        return 'fill=' + self.literal

    def size_evaluate(self):
        return 'height="%s"' % self.literal[0] + ' width="%s"' % self.literal[1]

    def upper_left_evaluate(self):
        return 'x="%s"' % self.literal[0] + ' y="%s"' % self.literal[1]

    def from_evaluate(self):
        return 'x1="%s"' % self.literal[0] + ' y1="%s"' % self.literal[1]

    def to_evaluate(self):
        return 'x2="%s"' % self.literal[0] + ' y2="%s"' % self.literal[1]

    def center_evaluate(self):
        return 'cx="%s"' % self.literal[0] + ' cy="%s"' % self.literal[1]

    def radius_evaluate(self):
        return 'radius="%s"' % self.literal

    def rx_evaluate(self):
        return 'rx="%s"' % self.literal

    def ry_evaluate(self):
        return 'ry="%s"' % self.literal

    def at_evaluate(self):
        return 'x="%s"' % self.literal[0] + ' y="%s"' % self.literal[1]

    def optional_text_parameter_evaluate(self):
        return self.parameter_name + '=' + self.literal[1:-1]

    def stroke_evaluate(self):
        return 'stroke=%s' % self.literal

    def stroke_width_evaluate(self):
        return 'stroke-width="%s"' % str(self.literal)
