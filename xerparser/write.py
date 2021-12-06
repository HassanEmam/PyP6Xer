# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.


import csv

def writeXER(r, filename):
    header = ['ERMHDR', '8.0', '2021-11-02', 'Project',	'admin', 'Primavera', 'Admin', 'dbxDatabaseNoName', 'Project Management', 'U.K.']
    with open(filename, 'w', newline='', encoding='utf-8') as output:
        tsv_writer = csv.writer(output, delimiter='\t')
        tsv_writer.writerow(header)
        tsv_writer.writerows(r.currencies.get_tsv())
        tsv_writer.writerows(r.fintmpls.get_tsv())
        tsv_writer.writerows(r.nonworks.get_tsv())
        tsv_writer.writerows(r.obss.get_tsv())
        tsv_writer.writerows(r.pcattypes.get_tsv())
        tsv_writer.writerows(r.resourcecurves.get_tsv())
        tsv_writer.writerows(r.udftypes.get_tsv())
        tsv_writer.writerows(r.accounts.get_tsv())
        tsv_writer.writerows(r.pcatvals.get_tsv())
        tsv_writer.writerows(r.projects.get_tsv())
        tsv_writer.writerows(r.calendars.get_tsv())
        tsv_writer.writerows(r.projpcats.get_tsv())
        tsv_writer.writerows(r.scheduleoptions.get_tsv())
        tsv_writer.writerows(r.wbss.get_tsv())
        tsv_writer.writerows(r.resources.get_tsv())
        tsv_writer.writerows(r.acttypes.get_tsv())
        tsv_writer.writerows(r.resourcerates.get_tsv())
        tsv_writer.writerows(r.activities.get_tsv())
        tsv_writer.writerows(r.actvcodes.get_tsv())
        # PROJCOST
        tsv_writer.writerows(r.relations.get_tsv())
        tsv_writer.writerows(r.taskprocs.get_tsv())
        tsv_writer.writerows(r.activityresources.get_tsv())
        tsv_writer.writerows(r.activitycodes.get_tsv())
        tsv_writer.writerows(r.udfvalues.get_tsv())
        tsv_writer.writerow(['%E'])

