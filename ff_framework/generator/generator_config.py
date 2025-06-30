from ff_framework.generator.generators import PDFGenerator

class GeneratorConfig:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database
        self.generators = {
            "PDFGenerator": PDFGenerator(logger, database)
        }
        
    def generate(self, generator_name, *args):
        if generator_name not in self.generators:
            self.logger.log(f"Generator {generator_name} not found.", level='error')
            raise ValueError(f"Generator {generator_name} not found.")
        
        self.logger.log(f"Generating with {generator_name}...", level='info')
        generator = self.generators[generator_name]
        return generator.generate(*args)