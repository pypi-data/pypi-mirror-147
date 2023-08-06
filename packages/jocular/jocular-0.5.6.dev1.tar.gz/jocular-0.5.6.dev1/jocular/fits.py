''' fits.py
    handles fits loading and editing
'''

from astropy.io import fits


class fits:


    def build_calibrations(self):
        ''' Contruct table from library
        '''

        return Table(
            size=Window.size,
            data=self.library,
            name='Calibration masters',
            description='Calibration masters',
            cols={
                'Name': {'w': 120, 'align': 'left', 'field': 'name', 
                'action': self.show_calibration_frame},
                'Camera': {'w': 140, 'align': 'left', 'field': 'camera', 'type': str},
                'Type': {'w': 60, 'field': 'type', 'align': 'left'},
                'Exposure': {'w': 80, 'field': 'exposure'},
                'Temp. C': {'w': 80, 'field': 'temperature', 'type': str},
                'Gain': {'w': 50, 'field': 'gain', 'type': int},
                'Offset': {'w': 60, 'field': 'offset', 'type': int},
                #'ROI': {'w': 80, 'field': 'ROI', 'type': str},
                'Bin': {'w': 45, 'field': 'bin', 'type': int},
                'Calib': {'w': 120, 'field': 'calibration_method', 'type': str},
                'Filter': {'w': 80, 'field': 'filter'},
                'Created': {'w': 120, 'field': 'created', 'sort': {'DateFormat': date_time_format}},
                'Size': {'w': 110, 'field': 'shape_str'},
                'Age': {'w': 50, 'field': 'age', 'type': int},
                'Subs': {'w': 50, 'field': 'nsubs', 'type': int}
                },
            actions={'move to delete dir': self.move_to_delete_folder},
            on_hide_method=self.app.table_hiding
            )

    def show_calibration_table(self, *args):
        ''' Called when user clicks 'library' on GUI
        '''

        if not hasattr(self, 'calibration_table'):
            self.calibration_table = self.build_calibrations()
        self.app.showing = 'calibration'

        # check for redraw
        if self.calibration_table not in self.app.gui.children:
            self.app.gui.add_widget(self.calibration_table, index=0)

        self.calibration_table.show()    

    def show_calibration_frame(self, row):
        self.calibration_table.hide()
        # convert row.key to str (it is numpy.str by default)
        # get image from path
        try:
            path = os.path.join(self.calibration_dir, str(row.key))
            im = Image(path)
            if im.sub_type == 'flat':
                im.image /= 2
            Component.get('Monochrome').display_sub(im.image)
        except Exception as e:
            logger.error('{:}'.format(e))


    def move_to_delete_folder(self, *args):
        objio = Component.get('ObjectIO')
        for nm in self.calibration_table.selected:
            if nm in self.library:
                objio.delete_file(os.path.join(self.calibration_dir, nm))
                del self.library[nm]
                del self.masters[nm]
        logger.info('deleted {:} calibration masters'.format(len(self.calibration_table.selected)))
        self.calibration_table.update()
