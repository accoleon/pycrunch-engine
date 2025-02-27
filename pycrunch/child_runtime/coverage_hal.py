import os

import coverage

from pycrunch.api.serializers import CoverageRunForSingleFile


COVER_LIBS = False

class CoverageAbstraction:
    cov: "coverage.Coverage"

    def __init__(self, disable,
                 coverage_exclusions,  # type: list[str]
                 timeline):
        """

        :type timeline: pycrunch.introspection.timings.Timeline
        :type disable: bool; coverage will be disabled inside debugging session
        """
        self.timeline = timeline
        self.disable = disable
        self.coverage_exclusions = coverage_exclusions
        self.cov = None

    def start(self):
        if self.disable:
            self.timeline.mark_event('Run: Coverage disabled. Do not start it.')
            return

        from . import exclusions

        use_slow_tracer = False
        # user_slow_tracer = True
        coverage_args = self.get_coverage_arguments()
        if COVER_LIBS:
            import site
            # Get the path to your virtual environment's site-packages
            site_packages_path = site.getsitepackages()[0]
            coverage_args["source"] = [site_packages_path, '.']

        # todo exclusion list should be configurable
        cov = coverage.Coverage(
            **coverage_args,
            config_file=False,
            timid=use_slow_tracer,
            branch=False,
            omit=exclusions.exclude_list + self.coverage_exclusions,
        )

        # logger.debug('-- before coverage.start')

        # !!!!!
        # debug will not work after cov.start is called!
        # !!!!!
        cov.start()

        # cov.exclude('def')

        # logger.debug('-- after coverage.start')
        self.timeline.mark_event('Run: Coverage started')
        self.cov = cov

    def stop(self):
        if self.disable:
            self.timeline.mark_event('Run: Coverage disabled. Cannot stop.')
            return

        self.cov.stop()
        self.timeline.mark_event('Coverage stopped')

    def get_coverage_arguments(self):
        coverage_args = dict()
        if self.is_coverage_v5_or_greater():
            # don't write on disk `.coverage` files,
            # it is not needed, and will be deadlocked due to concurrent test execution
            coverage_args.update(
                dict(
                    data_file=None
                ))
        return coverage_args

    def is_coverage_v5_or_greater(self):
        version_info = getattr(coverage, 'version_info', None)
        if not isinstance(version_info, tuple) or len(version_info) <= 0:
            return False

        return version_info[0] >= 5

    def parse_all_hit_lines(self):
        """
          Converts data from coverage.py format to internal format

          And plans are to integrate it with PyTrace Coverage
          But then pytrace should be optimized/compiled for multi-platform

          :rtype: typing.List[pycrunch.api.serializers.CoverageRunForSingleFile]
        """

        if self.disable:
            return []

        interim_results = []
        coverage_data = self.cov.get_data()
        for f in coverage_data.measured_files():
            # maybe leave only what we need?
            # TODO: look at numbits -> smart hash or what it is in coverage.py db
            #  maybe i will want to send it (encode this way)
            lines = coverage_data.lines(f)

            if len(lines) <= 0:
                continue

            # arcs = coverage_data.arcs(f)
            #         * The file name for the module.
            #         * A list of line numbers of executable statements.
            #         * A list of line numbers of excluded statements.
            #         * A list of line numbers of statements not run (missing from
            #           execution).
            #         * A readable formatted string of the missing line numbers.
            # analysis = cov.analysis2(f)
            # TODO or not todo?
            # f = normalize_path(f)

            interim_results.append(CoverageRunForSingleFile(f, lines))
        return interim_results
